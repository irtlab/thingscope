
from io import BytesIO

import sys
import argparse
import scapy.all as scapy
import time
import itertools
import json
import requests
from requests.packages.urllib3.connection import VerifiedHTTPSConnection
import pandas as pd
from sink import DeviceSink
import numpy as np
import logging
import logging.config
import queue
import threading
from aws_handler import *


#
# SecurityAnalyzer performs analysis on network packets by parsing DNS, ether, TCP/IP packets
# Finds out the remote endpoints,
# Finds out location and IP organization of the remote service
# For https protocol, it calls endpoint to retrieve details from the received certificate
#

class SecurityAnalyzer:
    def __init__(self, device_mac_address="", device_title="", sink=None, sink_interval=10, is_save_pcap=False, iface_mac_addr=None, ignore_mac_addrs="", internal_ip_prefix=""):
        self.domains = set()
        self.sink = sink
        self.device_title = device_title
        self.sink_interval_secs = sink_interval
        self.ip_domain_mapping = dict()  # store domain name of dest IP
        self.domain_cnames = dict()
        self.ip_tls_map = dict()
        self.domains_ip_timestamp = []  # store timestamp of access to domain name/IP
        self.protocols = set()
        self.device_id_db = None  # device ID in database
        self.device_dict = dict()  # dictionary of device information
        self.device_endpoints_store = dict()
        self.iot_servers = []
        self.last_sink_time = time.time()
        self.is_save_pcap = is_save_pcap
        self.ignore_macs = set()
        self.internal_ip_prefix = internal_ip_prefix
        for m in ignore_mac_addrs.split(","):
            self.ignore_macs.add(m)

        self.device_mac_address = device_mac_address
        self.recvd_pkts_count = 0
        self.processed_pkts_count = 0
        self.iface_mac_addr = iface_mac_addr
        self.device_meta_map = dict()
        self.pktq = queue.Queue()
        # list of devices seen right now
        self.devices = set()

        self.port_protocol_map = {
            '80/tcp' : 'http',
            '7104/tcp': 'http',
            '443/tcp': 'https',
            '8443/tcp': 'https',
            '7102/tcp': 'https',
            '7105/tcp': 'https',
            '1443/tcp': 'https',
            '22/tcp': 'ssh',
            '20/tcp': 'ftp',
            '21/tcp': 'ftp',
            '25/tcp': 'smtp',
            '1883/tcp': 'mqtt',
            '8883/tcp': 'mqtt secured',
            '53/tcp': 'dns',
            '53/udp': 'dns',
            '67/tcp': 'dhcp',
            '68/tcp': 'dhcp',
            '67/udp': 'dhcp',
            '68/udp': 'dhcp',
            '123/udp': 'ntp',
            '989/tcp': 'ftp secured',
            '989/tcp': 'ftp secured',
        }

        ioj = open('iana_openssl_mapping.json')
        data = json.load(ioj)
        self.openssl_iana_map = {v: k for k, v in data.items()}

        self.cipher_info_keys = ['key_exchange', 'auth_algo', 'encryption_algo', 'operation_auth_mode', 'hashing_algo']
        # list of non-IoT devices

    def add_to_device_list(self, device):
        # add device to list of devices seen
        self.devices.add(device)


    #
    # calls endpoint to retrieve details from the received certificate
    #
    def do_endpoint_security(self, endpoint):
        logging.info(f'Starting Endpoint Security On {endpoint}')
        debug_entries = []
        
        r = requests.get(endpoint, verify=False)
        SOCK = None
    
        _orig_connect = requests.packages.urllib3.connection.VerifiedHTTPSConnection.connect

        def _connect(self):
            global SOCK
            _orig_connect(self)
            SOCK = self.sock

        requests.packages.urllib3.connection.VerifiedHTTPSConnection.connect = _connect
        tlscon = SOCK.connection
        cipher_name = tlscon.get_cipher_name()
        cipher_version = tlscon.get_cipher_version()
        return cipher_name, cipher_version

        # logging.debug('Output of GET request:\n%s' % get_body.decode('utf8'))

    def identify_security_posture(self, endpoint_info, pkt):
        endpoint_info['security_posture'] = 'unknown'

    #
    # Returns a dictionary containing info about the payload type
    #
    #     Top level key is type. Other keys in dictionary depend on type.
    #         aka 'type':16 = TLS Hello handshake
    #             'type':17 = TLS application data section
    #
    # Returns None, if the data was invalid for a TLS payload type
    #
    def identify_tls_payload_type(self, pkt):
        try:
            if not hasattr(pkt, 'load'):
                return None
            packet_section = pkt.load.hex()
            ## Note, the record header should be at the very begining of the sections
            result = {}

            # Data sanity check
            if packet_section == None:
                logging.warning("null packet")
                return None

            if len(packet_section) < 6:
                # logging.warning("Too small packet")
                return None

            # Quick bail out if not a supported TLS type, (all start with '1')
            if packet_section[0] != '1':
                return None

            ## Check the protocol version
            if packet_section[2:5] != '030':
                # Invalid TLS protocol number
                return None

            # TLS 1.0 (wow old). See it sometimes in the initial client hello
            if packet_section[5] == '1':
                result['tls_version'] = '1.0'
            # TLS 1.1 (still old)
            elif packet_section[5] == '2':
                result['tls_version'] = '1.1'
            # TLS 1.2 (currently all that is supported for this tool)
            elif packet_section[5] == '3':
                result['tls_version'] = '1.2'
            # TLS 1.3
            elif packet_section[5] == '4':
                result['tls_version'] = '1.3'
            # Unsupported TLS type
            else:
                logging.warning("invalid TLS protocol number, (version)")
                return None

            # Default value, should be overridden by each section as I add the parsing
            # for it
            result['next_section'] = 6

            ## Check section type

            # Change cipher spec
            if packet_section[1] == '4':
                result['type'] = 14

            # Alert record
            elif packet_section[1] == '5':
                result['type'] = 15

            # If a hello handshake (starts with '16')
            elif packet_section[1] == '6':
                result['type'] = 16

                result['next_section'] += int(packet_section[6:10], 16)

                ## Get the handshake type
                if packet_section[10:12] == "01":
                    result['sub_type'] = "client_hello"

                elif packet_section[10:12] == "02":
                    result['sub_type'] = "server_hello"

                    # Advance through the packet:
                    cur_section = packet_section[22:]

                    # Server random number. Starts with timestamp sometimes
                    # not currently using this
                    server_random = cur_section[:64]
                    cur_section = cur_section[64:]

                    # Session id for restarting sessions
                    # not currently using this
                    session_id_len = int(cur_section[0:2], 16)
                    session_id = cur_section[2:2 + session_id_len * 2]

                    # Grab the cipher suite selection which is what this application
                    # really cares about
                    cur_section = cur_section[2 + (session_id_len * 2):]
                    cipher_suite = cur_section[0:4]
                    result['cipher'] = cipher_suite

                    # Grab the compression method which will also be important for
                    # doing traffic analysis
                    compression_method = cur_section[4:6]
                    result['compression'] = compression_method

                elif packet_section[10:12] == "0b":
                    result['sub_type'] = "server_certificate"

                elif packet_section[10:12] == "0e":
                    result['sub_type'] = "server_hello_done"

                else:
                    # logging.warning("Don't know what type of hello packet this is")
                    # logging.warning( packet_section[10:12])
                    return None

            # If application data section (starts with '17')
            elif packet_section[1] == '7':
                result['type'] = 17
                result['next_section'] += int(packet_section[6:10], 16)

                ## Find out how much application data is being sent
                result['app_data_size'] = int(packet_section[6:10], 16)

            # Unsupported type
            else:
                logging.warning("Unsupported type")
                logging.warning(packet_section[0:5])
                return None
            ret_result = {}
            ret_result['tls_version'] = result['tls_version']
            if 'app_data_size' in result:
                ret_result['app_data_size'] = result['app_data_size']
            return ret_result
        except Exception as e:
            logging.error(f'post processing exception for {e}' + str(e))
            return None

    #
    # Protocol Handler, runs on separate thread. Does not blocl main sniffing thread
    # Calls various functions to understand domain names, security posture of the endpoint
    #
    def protocol_handler_v2(self, pkt):

        mac_addr_src = str(pkt[scapy.Ether].src)
        mac_addr_dst = str(pkt[scapy.Ether].dst)

        # Only check packets coming from target device for protocol information
        if self.device_mac_address and mac_addr_src != self.device_mac_address:
            return

        port_proto = None
        protocol = None
        if scapy.IP in pkt:
            device_ip = str(pkt[scapy.IP].src)
            if device_ip != '0.0.0.0':
                self.device_meta_map[mac_addr_src] = device_ip

        if scapy.UDP in pkt:
            port_proto = str(pkt[scapy.UDP].dport) + "/" + "udp"
            self.protocols.add(port_proto)
            protocol = 'udp'
        try:
            if scapy.TCP in pkt:
                port_proto = str(pkt[scapy.TCP].dport) + "/" + "tcp"
                if (port_proto == "443/tcp"):
                    tls_result = self.identify_tls_payload_type(pkt)
                    if tls_result:
                       self.ip_tls_map[str(pkt[scapy.IP].dst)] = tls_result
        except IndexError as e:
            logging.warning("Unexpected exception during identification of tls payload type")

            self.protocols.add(port_proto)
            protocol = 'tcp'

        layers = list(layer_expand(pkt))
        protocol = self.port_protocol_map.get(port_proto, protocol)

        # dhcp ports 67 68/ dns ports 53, 5353 multicast DNS
        if port_proto is None or port_proto in ['5353/udp', '67/udp', '53/udp', '4096/udp', '68/udp']:
            return None

        endpoint_info = dict()
        endpoint_info['port'] = port_proto
        endpoint_info['protocol'] = protocol
        if 'IP' in layers:
            endpoint_info['ip'] = str(pkt[scapy.IP].dst)
        return endpoint_info

    def get_protocol(self, port_proto):
        return None

    #
    # Calls ipapi.co by passing the ip address
    # retireves city, region, country, coordinates, ip org
    #
    def get_location(self, ip_address):
        try:
            r = requests.get(f'http://api.ipapi.com/{ip_address}?access_key=fb54484407554c0b896022c5e732c125')
            if 'ip' in r.json():
                return r.json()
        except:
            logging.error("Error accessing location data from ipapi")
            return None


    #
    # updates cipher info
    #
    def update_cipher_info(self, ip, endpoint_map, cipher_info):
        for k in cipher_info.keys():
            val = cipher_info[k]
            endpoint_map[ip][k] = val

    def get_orig_domain(self, domain):
        if self.domain_cnames.__contains__(domain):
            return domain

        for d in self.domain_cnames.keys():
            cnames = self.domain_cnames.get(d)
            if domain in cnames:
                return d
        return domain

    def sink_domain_maps(self):
        for d in self.domain_cnames.keys():
            cnames = self.domain_cnames.get(d)
            self.sink.save_domain_map(d, list(cnames))

    def postProcess(self):
        logging.debug(f'Sink Started')
        ip_domain_map = {}
        df = pd.DataFrame.from_records(self.iot_servers)
        df = df.drop_duplicates()

        logging.debug(df)
        if not df.empty:
            for index, group in df.groupby('ip'):
                domains = group['dns_name'].tolist()
                logging.debug(f'index {index } group {domains}')
                ip_domain_map[index] = max(domains, key= len)

        logging.info(f'ip_domain_map {ip_domain_map}')
        logging.info(f'domain_cnames {self.domain_cnames}')

        for device_mac in self.device_endpoints_store:
            endpoints_map = self.device_endpoints_store[device_mac]
            for ip in endpoints_map.keys():
                try:
                    if ip == 'debug_me':
                        logging.debug('wait')

                    if self.sink and self.sink.is_endpoint_exist(ip):
                        continue

                    if ip in ip_domain_map:
                        domain_name = ip_domain_map[ip]
                        orig_domain = self.get_orig_domain(domain_name)
                        endpoints_map[ip]['domain_name'] = domain_name
                        endpoints_map[ip]['orig_domain'] = orig_domain

                    if ip in self.ip_tls_map:

                        endpoints_map[ip]['tls_version'] = self.ip_tls_map[ip].get('tls_version', '')
                        endpoints_map[ip]['security_posture'] = "encrypted"
                        try:
                            if ip in ip_domain_map:
                                domain_name = ip_domain_map[ip]
                                cipher_name, cipher_version = security_analyzer.do_endpoint_security('https://' + str(domain_name))
                                #endpoints_map[ip]['self_signed'] = self_signed
                                endpoints_map[ip]['openssl_name'] = cipher_name
                                endpoints_map[ip]['cert_tls_version'] = tls_version
                        except Exception as e:
                            logging.error(f'post processing exception for {ip} {e}')

                    if not any(str(ip).startswith(item) for item in self.internal_ip_prefix):
                        location_data = self.get_location(ip)
                        logging.debug(f'{ip} location {location_data}')
                        endpoints_map[ip]['location'] = location_data

                    if self.sink:
                        self.sink.save_endpoint(device_mac=device_mac, endpoint_info=endpoints_map[ip])

                except Exception as e:
                    logging.error(f'post processing exception for {ip} {e}')

        for device in self.device_meta_map.keys():
            if self.sink and self.sink.is_device_exist(device):
                continue

            if self.sink:
                name='TBD'
                if not self.device_mac_address:
                    name = self.device_title
                sink.save_device(device, self.device_meta_map[device], name=name)
        if self.sink:
            self.sink_domain_maps()

    def printStore(self):
        logging.info(json.dumps(self.device_endpoints_store, indent=3, sort_keys=True))

    def is_endpoint_exist(self, device_mac, ip):
        if not self.device_endpoints_store.__contains__(device_mac):
            return False
        return self.device_endpoints_store[device_mac].__contains__(ip)

    def add_device_endpoint(self, device_mac, ip, endpoint_info):
        if not self.device_endpoints_store.__contains__(device_mac):
            self.device_endpoints_store[str(device_mac)] = dict()
        endpoint_map = self.device_endpoints_store[device_mac]
        if endpoint_map is None:
            self.device_endpoints_store[device_mac] = dict()
        self.device_endpoints_store[device_mac][ip] = endpoint_info


    def gen_pcap_filename(self, mac):
        return "pcap_database/{mac}.pcap".format(mac=mac)

    def get_device_mac_addr(self, src_mac_addr, dst_mac_addr):
        if self.device_mac_address:
            return self.device_mac_address

        if src_mac_addr and src_mac_addr == self.iface_mac_addr:
            return dst_mac_addr
        if dst_mac_addr and dst_mac_addr == self.iface_mac_addr:
            return src_mac_addr
        return None

    def pktq_consumer(self):
        time_since_last_log = time.time()
        logging.info('Starting pkt q consumer')
        while True:
            pkt = self.pktq.get()

            if ( time.time() - time_since_last_log > 5):
                logging.info(f'pktq size {self.pktq.qsize()} {pkt.summary()} total recvd pkts {self.recvd_pkts_count} total processed pkts {self.processed_pkts_count}')
                time_since_last_log = time.time()

            self.pktHandler(pkt)

            self.pktq.task_done()
            self.processed_pkts_count += 1

    def pktq_producer(self, pkt):
        self.recvd_pkts_count += 1
        self.pktq.put(pkt)


    def pktHandler(self, pkt):

        try:
            #logging.info(pkt.summary())
            if not pkt.haslayer(scapy.Ether):
                return

            src_mac_addr = str(pkt[scapy.Ether].src)
            dst_mac_addr = str(pkt[scapy.Ether].dst)

            mac_addr = self.get_device_mac_addr(src_mac_addr, dst_mac_addr)

            if not mac_addr:
                return

            
            #logging.info(f'device {mac_addr}')

            if self.ignore_macs.__contains__(mac_addr):
                return

            if self.is_save_pcap:
                self.write_pcap(self.gen_pcap_filename(mac_addr), pkt)

            # Handle packet
            endpoint_info = self.protocol_handler_v2(pkt)


            if endpoint_info and endpoint_info.get('ip'):
                endpoint_ip = endpoint_info['ip']
                if not self.is_endpoint_exist(mac_addr, endpoint_ip):
                    self.identify_security_posture(endpoint_info, pkt)
                    self.add_device_endpoint(mac_addr, endpoint_ip, endpoint_info)

            self.dns_callback(pkt)

            time_since_last_sink = (time.time() - self.last_sink_time)
            if time_since_last_sink >= self.sink_interval_secs:
                self.postProcess()
                self.last_sink_time = time.time()

        except Exception as e:
            logging.exception("Unexpected exception during pkt handling ! %s %s", e, str(pkt))


    def dns_callback(self, pkt):

        def get_dest_ip(packet):
            if packet.haslayer(scapy.IP):
                return packet[scapy.IP].dst
            else:
                return ""

        def clean_endpoint(e):
            e = e.replace("b'", "")
            e = e.replace("'\n","")
            e = e.replace("\.'", "")
            e = e.replace(".'", "")
            return e

        def process_dns_packet(packet):
            #logging.info(packet.show())
            if packet.haslayer(scapy.DNSRR) and packet[scapy.DNSRR].type == 1:  # 1 is stands for 'A' DNS record
                dest_ip = get_dest_ip(packet)
                domain_name = packet[scapy.DNSRR].rrname
                domain_ip_address = packet[scapy.DNSRR].rdata
                logging.debug('****[DNS-A]\t' + str(dest_ip) + ' <<< ' + str(domain_name) + ' (' + str(domain_ip_address) + ')')
            if packet.haslayer(scapy.DNSRR) and packet[scapy.DNSRR].type == 5:  # 1 is stands for 'CNAME' DNS record
                dest_ip = get_dest_ip(packet)
                domain_name = str(packet[scapy.DNSRR].rrname)
                cname = str(packet[scapy.DNSRR].rdata)
                logging.debug('****[DNS-CNAME]\t' + str(dest_ip) + ' <<< ' + domain_name + ' (' + cname + ')')
                cnames = self.domain_cnames.get(domain_name)
                if not cnames:
                    cnames = set()
                cnames.add(cname)
                self.domain_cnames[domain_name] = cnames


        #try:
            if pkt.haslayer(scapy.DNS):
                ancount = pkt[scapy.DNS].ancount
                i = ancount + 4
                while i > 4:
                    if pkt[0][i].type == 1:
                        self.iot_servers.append({'dns_name': clean_endpoint(str(pkt[0][i].rrname)), 'ip': pkt[0][i].rdata})
                    i -= 1
                process_dns_packet(pkt[scapy.DNS])
        #except Exception as e:
        #    logging.warning(f'DNS packet local')

    def write_pcap(self, pcap_filename, pkt):
        scapy.wrpcap(pcap_filename, pkt, append=True)

    async def produce_write_pkt(self, pcap_filename, pkt) -> None:
        await self.writeq.put((pcap_filename, pkt))

    async def consume_writeq(self):
        while True:
            pcap_filename, pkt = await self.writeq.get()
            scapy.wrpcap(pcap_filename, pkt, append=True)
            self.writeq.task_done()

#
# Read pcap file, calls pktHnadler for each packet
# performs post processing on the accumulated data structure
#
def process_pcap(pcapf, internal_ip_prefix):
    packets = scapy.rdpcap(pcapf)
    unique_macs = list(set([x.src for x in packets]))
    logging.info(unique_macs)
    for mac in unique_macs:
        logging.info(f"\nNow processing {mac}")
        security_analyzer = SecurityAnalyzer(device_mac_address=mac, internal_ip_prefix=internal_ip_prefix)
        for pkt in packets:
            security_analyzer.pktHandler(pkt)
    security_analyzer.postProcess()
    security_analyzer.printStore()

### helper functions ###

# expand the packet to check for DNS type
def layer_expand(packet):
    yield packet.name
    while packet.payload:
        packet = packet.payload
        yield packet.name

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()

    parser.add_argument("--pcap", help="pcap file to process", default="", required=False)
    parser.add_argument("--db_url", help="DB Connection Endpoint", default="mongodb://localhost:27017/", required=False)
    parser.add_argument("--db_name", help="DB Name", default="iot", required=False)
    parser.add_argument("--title", help="Device Title to save. Useful when you are processing single pcap file. Otherwise, you will have to update device title through Web UI", default="", required=False)
    parser.add_argument("--save_pcap", help="Enable Pcap file saving to create pcap file. Useful when processing live network traffic.", action='store_true', required=False)
    parser.add_argument("--disable_sink", help="Disable Sink. This will just print final Device Endpoint map.", action='store_true', required=False)
    parser.add_argument("--ignore_mac_addrs", help="Comma separated list of mac addresses to ignore", default="", required=False)
    parser.add_argument("--internal_ip_prefix", help="Internal ip prefixes (as list)", default=["10.", "192.168.", "255.255.255.255"], required=False)

    parser.add_argument("--iface_mac_addr", help="Interface Mac address", default="",
                        required=False)

    #group = parser.add_mutually_exclusive_group(required=True)
    #group.add_argument("--devmacaddr", help="MAC address of IoT device if you want to process only single IoT Device from pacap file", default="", required=False)
    #group.add_argument("--iface", help="Interface to listen", default=None, required=False)
    parser.add_argument("--iface", help="Interface to listen", default=None, required=False)


    parser.add_argument("--sink_interval", help="Sink Interval in seconds. While processing live network stream, how often do you want to update database", default=10, required=False)

    args = parser.parse_args()


    sink = None
    if not args.disable_sink:
        sink = DeviceSink(db_url=args.db_url, db_name=args.db_name)


    #security_analyzer = SecurityAnalyzer(device_mac_address=args.devmacaddr, device_title= args.title, sink=sink, sink_interval=args.sink_interval,
    #                                     is_save_pcap=args.save_pcap, iface_mac_addr=args.iface_mac_addr, ignore_mac_addrs=args.ignore_mac_addrs,
    #                                     internal_ip_prefix=args.internal_ip_prefix)


    try:

        # Pcap file processing mode
        if args.iface is None:
            logging.info(f'Processing pcap file {args.pcap}')
            process_pcap(args.pcap, args.internal_ip_prefix)

        # Realtime sniffing mode
        else:
            threading.Thread(target=security_analyzer.pktq_consumer, daemon=True).start()
            logging.info(f'Sniffing packets on {args.iface}')
            scapy.sniff(prn=security_analyzer.pktq_producer, iface=args.iface)

    except Exception as e:
        logging.error(f"[ERROR]: {e}")
