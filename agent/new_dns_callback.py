from scapy.all import *
import dpkt
from subprocess import call
import sqlite3
import datetime
import time
import json
import upload_to_db
from colorprint import ColorPrint as color
from iptable_controller import obtainMudProfile
from update_ip import update_device_domains
from IoT_Classification import get_device_dhcp_info


# TODO: LOOK FOR ENCRYPTION, HOW OFTEN COMMS OCCUR
# TODO: RUN WITH MULTIPLE DEVICES
# TODO: OBTAIN MANUFACTURER INFO FROM WHOIS/WIRESHARK

# save pcap for further analysis
pcap_filename = str(datetime.datetime.now()) + "____pcap_file.pcap"

class DNSCallback:
    def __init__(self, device_name="", device_model="", manufacturer_name="", manufacturer_website="", ignore_device=""):
    
        # initialise device information
        self.device_name = device_name
        self.device_model = device_model
        self.manufacturer_name = manufacturer_name
        self.manufacturer_website = manufacturer_website
        self.domains = set()
        self.ip_domain_mapping = dict()                     # store domain name of dest IP
        self.domains_ip_timestamp = []              # store timestamp of access to domain name/IP
        self.protocols = set()
        self.device_id_db = None                            # device ID in database
        self.device_dict = dict()                           # dictionary of device information
        
        # update/init dictionary of device information
        self.update_device_dict()

        # list of devices seen right now
        self.devices = set()
        # list of non-IoT devices
        self.ignore_devices = set()
        if ignore_device:
            self.ignore_devices.add(ignore_device)

        # monitor network flow list
        self.DELTA_TIME = datetime.timedelta(seconds = 30)
        self.START_TIME = datetime.datetime.now()

        # create pcap file
        pcap_file = open(pcap_filename, "w+")

        # store IP of gateway/router
        self.ROUTER_IP = ''

    def add_to_device_list(self, device):
        # add device to list of devices seen
        self.devices.add(device)
    def add_to_ignore_device_list(self, ignore_device):
        # add device to list of devices to be ignored
        self.ignore_devices.add(ignore_device)

    def update_device_dict(self):

        # device_dict['mac_address'] = pkt[Ether].dst
        # device_dict['ip_address'] = pkt.getlayer(IP).dst

        self.device_dict['device'] = self.device_name
        self.device_dict['device_model'] = self.device_model
        # self.device_dict['domains'] = list(self.domains)
        self.device_dict['domains'] = self.domains_ip_timestamp
        self.device_dict['protocols'] = list(self.protocols)

        manufacturer_dict = dict()
        manufacturer_dict['name'] = self.manufacturer_name
        manufacturer_dict['website'] = self.manufacturer_website
        self.device_dict['manufacturer'] = manufacturer_dict

    def protocol_handler(self, pkt):
        
        mac_addr = str(pkt[Ether].src)
        
        # Only check packets coming from target device for protocol information
        if mac_addr not in self.ignore_devices:

            if UDP in pkt:
                protocol = str(pkt[UDP].dport) + "/" + "udp"
                self.protocols.add(protocol)
            if TCP in pkt:
                protocol = str(pkt[TCP].dport) + "/" + "tcp"
                self.protocols.add(protocol)

    def domain_timestamp_handler(self, pkt):

        if not IP in pkt:
            return
        
        dst_ip = str(pkt[IP].dst)
        if dst_ip == self.ROUTER_IP:
            return
        
        domain_qname = dst_ip
        pkt_timestamp = int(time.time())
    
        if dst_ip in self.ip_domain_mapping:
            domain_qname = self.ip_domain_mapping[dst_ip]
    
        # add timestamp to domain_ip_timestamp
        for domain_entry in self.domains_ip_timestamp:
            if domain_qname == domain_entry['name']:
                ip_list = domain_entry['ip_addr']
                if dst_ip in ip_list:
                    if ip_list.index(dst_ip) in domain_entry['timestamps']:
                        domain_entry['timestamps'][ip_list.index(dst_ip)].append(pkt_timestamp)
                    else:
                        domain_entry['timestamps'][ip_list.index(dst_ip)] = [pkt_timestamp]


    def pktHandler(self, pkt):

        try:
            mac_addr = str(pkt[Ether].src)
            write_pcap(pkt)                 # write to pcap file to analyse later if needed
            
            if mac_addr not in self.ignore_devices:
                if datetime.datetime.now() - self.START_TIME > self.DELTA_TIME:
                    # Update device dictionary
                    self.update_device_dict()
                    # print("Uploading: " + str(self.device_dict))

                    # Update database
                    if self.device_id_db is None:
                        try:
                            self.device_id_db, insert_response = upload_to_db.insert_in_db(self.device_dict)
                            print(color.OKGREEN + "[INFO] Insert in database: Successful!" + color.ENDC)
                            # print(insert_response)
                        except Exception as e:
                            print(color.ERROR + "[ERROR] Insert in database: Failed!\nERROR: " + str(e) + color.ENDC)
                    else:
                        try:
                            # print(upload_to_db.get_devices_from_db())
                            upload_response = upload_to_db.update_in_db(self.device_id_db, self.device_dict)
                            print(color.OKGREEN + "[INFO] Update in database: Successful!" + color.ENDC)
                            # print(upload_response)
                        except Exception as e:
                            print(color.ERROR + "[ERROR] Update in database: Failed!\nERROR: " + str(e) + color.ENDC)
                    
                    # Reset measurements
                    self.START_TIME = datetime.datetime.now()
                    # self.domains_frequency = dict()

            # Handle packet    
            self.protocol_handler(pkt)
            self.standard_dns_callback(pkt)
            self.domain_timestamp_handler(pkt)
        
        except Exception as e:
            print(color.ERROR + "[ERROR] Exception while handling pkt: " + str(e) + color.ENDC)

    def standard_dns_callback(self, pkt):

        layers = list(layer_expand(pkt))

        if "DNS" in layers:
            self.dns_callback(pkt)
        elif "BOOTP" in layers:
            try:
                features = get_device_dhcp_info(pkt)
            except Exception as e:
                print("[ERROR] Unable to obtain features: " + str(e))

            mac_addr = str(pkt[Ether].src)
            self.ROUTER_IP = str(pkt[IP].dst)
            if not features['IoT']:
                # General Purpose device
                # print("[INFO] " + str(features))
                print(color.OKCYAN + "-----[INFO] General Purpose Device-----" + color.ENDC)
                # Ignore packets from this device
                self.add_to_ignore_device_list(mac_addr)
            else:
                # print("BOOTP: " + mac_addr)
                # mac_addr = str(pkt[Ether].src)
                print(color.OKCYAN + "-----[INFO] IoT Device-----" + color.ENDC)
                self.START_TIME = datetime.datetime.now()
                try:
                    if mac_addr not in self.devices:
                        self.add_to_device_list(mac_addr)
                    else:
                        pass
                except Exception as e:
                    print ("[ERROR] Exception when dealing with MAC_ADDR: " + str(e))
        else:
            pass

    # confirm DNS ans packet and parse for info
    def dns_callback(self, pkt):

        if DNS in pkt and 'Ans' in pkt.summary():
            response = []

            for x in xrange(pkt[DNS].ancount):
                #capture the data in res packet
                if pkt[DNSRR][x].rdata:
                    response.append(pkt[DNSRR][x].rdata)

            try:
                domain_qname = pkt[DNSQR].qname
                if not domain_qname in self.domains:
                    print("[INFO] New Endpoint Detected: " + str(domain_qname))
                    # store all ip addresses associated with this QNAME
                    domain_dict = {'name': domain_qname, 'ip_addr': response, 'timestamps': {}}
                    self.domains_ip_timestamp.append(domain_dict)
                    for rdata in response:
                        self.ip_domain_mapping[rdata] = domain_qname
                self.domains.add(domain_qname)

            except Exception as e:
                print(color.ERROR + "[ERROR] Unable to update domain and/or frequencies. \nERROR: " + str(e) + color.ENDC)
                return


### helper functions ###

#expand the packet to check for DNS type
def layer_expand(packet):
    yield packet.name
    while packet.payload:
        packet = packet.payload
        yield packet.name

def write_pcap(pkt):
    wrpcap(pcap_filename, pkt, append=True)