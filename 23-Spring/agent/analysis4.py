#!/usr/bin/env python

import requests
#import argparse
#import json
#import os
import socket
from collections import defaultdict
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR

queries = defaultdict(list)
answers = defaultdict(list)
hosts = {}
IGNORE_PORTS = {80, 443, 8080}

#def get_args():
#    parser = argparse.ArgumentParser(description='Extract DNS and host data from pcap file.')
#    parser.add_argument('pcap_file', type=str, help='Path to pcap file')
#    #parser.add_argument('--parallel', action='store_true', help='Enable parallel processing')
#    return parser.parse_args()

def get_ip_location(ip):
    try:
        response = requests.get(f"http://api.ipapi.com/api/{host_ip}?access_key={ipapi_key}")
        if response.status_code == 200:
            data = response.json()
            return f'{data["city"]}, {data["country"]}'
    except:
        pass
    return ''

def process_packet(packet):
    if not packet.haslayer(IP) or not packet.haslayer(TCP):
        return None

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    src_mac = packet.src
    dst_mac = packet.dst
    src_port = packet[TCP].sport
    dst_port = packet[TCP].dport
    data_len = len(packet[TCP].payload)

    if src_ip == '127.0.0.1' or dst_ip == '127.0.0.1':
        return None

    if src_ip == '0.0.0.0' or dst_ip == '0.0.0.0':
        return None

    if src_ip == dst_ip:
        return None

    if packet.haslayer(DNS):
        dns = packet[DNS]
        if dns.qr == 0:
            queries[dns.qd.qname.decode('utf-8')].append((src_ip, dst_ip))
        else:
            for answer in dns.an:
                if isinstance(answer, DNSRR) and answer.type == 1:
                    query = answer.rrname.decode('utf-8')
                    answers[query].append((answer.rdata, src_ip, dst_ip))

    if src_ip not in hosts:
        try:
            hostname = socket.gethostbyaddr(src_ip)[0]
        except:
            hostname = ''
        hosts[src_ip] = {
            'hostname': hostname,
            'mac_address': src_mac,
            'open_tcp_ports': set(),
            'sent_data': 0,
            'received_data': 0,
            'incoming_sessions': defaultdict(int),
            'outgoing_sessions': defaultdict(int),
            'ip_location': get_ip_location(src_ip),
        }
    if dst_ip not in hosts:
        try:
            hostname = socket.gethostbyaddr(src_ip)[0]
        except:
            hostname = ''
        hosts[dst_ip] = {
            'hostname': hostname,
            'mac_address': dst_mac,
            'open_tcp_ports': set(),
            'sent_data': 0,
            'received_data': 0,
            'incoming_sessions': defaultdict(int),
            'outgoing_sessions': defaultdict(int),
            'ip_location': get_ip_location(dst_ip),
        }

    hosts[src_ip]['sent_data'] += data_len
    hosts[dst_ip]['received_data'] += data_len
    hosts[src_ip]['outgoing_sessions'][(dst_ip, dst_port)] += 1
    hosts[dst_ip]['incoming_sessions'][(src_ip, src_port)] += 1
    if dst_port not in IGNORE_PORTS:
        hosts[src_ip]['open_tcp_ports'].add(dst_port)
    if src_port not in IGNORE_PORTS:
        hosts[dst_ip]['open_tcp_ports'].add(src_port)


def betaMain(pcap_file):
    packets = rdpcap(pcap_file)
    for packet in packets:
        process_packet(packet)

    output_data = {
        'dns_queries': [{'query': query, 'answers': answers[query], 'count': len(queries[query])} for query in queries],
        'hosts': [{'ip': ip, **hosts[ip]} for ip in hosts],
    }

     def serialize(obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, tuple):
            return str(obj)
        else:
            raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")

    output_data = {
        'dns_queries': [{'query': query, 'answers': answers[query], 'count': len(queries[query])} for query in queries],
        'hosts': [{'ip': ip, **{k: serialize(v) if isinstance(v, set) else v for k, v in hosts[ip].items()}} for ip in hosts],
    }

#if __name__ == '__main__':
#    queries = defaultdict(list)
#    answers = defaultdict(list)
#    hosts = {}
#    IGNORE_PORTS = {80, 443, 8080}
#
#    args = get_args()
#
#    packets = rdpcap(args.pcap_file)
#    for packet in packets:
#        process_packet(packet)
#
#    pcap_name, pcap_ext = os.path.splitext(args.pcap_file)
#    output_file = f'{pcap_name}.json'
#    output_data = {
#        'dns_queries': [{'query': query, 'answers': answers[query], 'count': len(queries[query])} for query in queries],
#        'hosts': [{'ip': ip, **hosts[ip]} for ip in hosts],
#    }
#
#
#    def serialize(obj):
#        if isinstance(obj, set):
#            return list(obj)
#        elif isinstance(obj, tuple):
#            return str(obj)
#        else:
#            raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")
#
#    output_data = {
#        'dns_queries': [{'query': query, 'answers': answers[query], 'count': len(queries[query])} for query in queries],
#        'hosts': [{'ip': ip, **{k: serialize(v) if isinstance(v, set) else v for k, v in hosts[ip].items()}} for ip in hosts],
#    }

#    with open(output_file, 'w') as f:
#        for k, v in output_data.items():
#            if not isinstance(k, tuple):
#                f.write(str(k) + '\n')
#                for line in v:
#                    f.write('\t' + str(line) + '\n')


    
#    print(f'Data written to {output_file}.')




