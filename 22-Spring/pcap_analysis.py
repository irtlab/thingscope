'''

authors: Lama, Lin

Device Fingerprint, it takes as input pcaps and tests each packets against 23 features:


Link layer protocol (2)                 ARP/LLC
Network layer protocol (4)              IP/ICMP/ICMPv6/EAPoL
Transport layer protocol (2)            TCP/UDP
Application layer protocol (8)          HTTP/HTTPS/DHCP/BOOTP/SSDP/DNS/MDNS/ NTP
IP options (2)                          Padding/RouterAlert
Packet content (2)                      Size (int)/Raw data
IP address (1)                          Destination IP counter (int)
Port class (2)                          Source (int) / Destination (int)

usage : python pcap_analysis.py --pcap <pcap file>
example : 
'''

import argparse
import glob, os
import sys
from telnetlib import IP
from typing import Protocol
from scapy.utils import RawPcapReader
from scapy.all import *
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import sqlite3 as sq
import datetime
import time
import getopt
import socket
from struct import *


def pandas_to_sqllight(table):
    data = table
    sql_data = '/Users/lama/pcap.sqlite' #- Creates DB names SQLite
    conn = sq.connect(sql_data)
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS PCAP''')
    data.to_sql('PCAP', conn, if_exists='replace', index=False) 
    sql_data = pd.read_sql('select * from PCAP', conn)
    #print(sql_data)
    conn.commit()
    conn.close()




def read_pcap(file_name):
    scapy_cap = rdpcap(file_name)
    sessions = scapy_cap.sessions()
    print('{} contains {} packets'.format(file_name, len(scapy_cap)))
    print(scapy_cap)
    print("############## Packet Summary ##############")
    # print(scapy_cap.summary())
    print_summary(scapy_cap)
    print("############## Session Summary ##############")
    inter_arrival_time(sessions)
       


def print_summary(pkt):
    Summary_table = pd.DataFrame(columns = ["IP_src","IP_dst","Protocl", "Packet-size","Time"])
    list = []
    for p in pkt: 
        if IP in p:
            ip_src=p[IP].src
            ip_dst=p[IP].dst
            proto = p.sprintf("%IP.proto%")
            time = p.sprintf("%IP.time%")
            size = p.sprintf("%IP.len%")
            list.append({'IP_src':ip_src,'IP_dst':ip_dst,'Protocl': proto, 'Packet-size':size, "Time":time})

    Summary_table = Summary_table.append(list)
    print(Summary_table)
   # pandas_to_sqllight(Summary_table)


def inter_arrival_time(sessions):
    sessions_table = pd.DataFrame(columns = ["IP_src","sport","Protocl","IP_dst","dport", "Total-Packets","Direction","Time"])
    list = []
    i =0 
    flow_duration = []

    for k, v in sessions.items():
        if i >= 1: 
            tot_packets = len(v)
            try:
                proto, source, dir, target = k.split()
            except ValueError:
                continue 
            if(proto=="UDP" or proto =="TCP"):
                srcip, srcport = source.split(":")
                dstip, dstport = target.split(":")
            else:
                srcip, srcport = source,""
                dstip, dstport = target,""
            if dir == '>':
             direction="outbound"
            else:
             direction="inbound"
            pkttime = v[0].time
            list.append({'IP_src':srcip, "sport":srcport ,'Protocl':proto, "IP_dst":dstip,'dport': dstport, 'Total-Packets':tot_packets,"Direction":direction, "Time":pkttime})
        i += 1 
    sessions_table  = sessions_table .append(list)

    print(sessions_table)


# def parse_netflow(pkt):  
#     # grabs 'netflow-esqe' fields from packets in a PCAP file
#     try:
#         type = pkt.getlayer(IP).proto
#     except:
#         pass

#     snifftime = datetime.fromtimestamp(pkt.time).strftime('%Y-%m-%d %H:%M:%S').split(' ')[1]

#     if type == 6:
#         type = 'TCP'
#     if type == 17:
#         type = 'UDP'
#     if type == 1:
#         type = 'ICMP'

#     if type == 'TCP' or type == 'UDP':
#         print( ' '.join([snifftime, type.rjust(4, ' '), str(pkt.getlayer(IP).src).rjust(15, ' ') , str(pkt.getlayer(type).sport).rjust(5, ' ') , '-->' , str(pkt.getlayer(IP).dst).rjust(15, ' ') , str(pkt.getlayer(type).dport).rjust(5, ' ')]))

#     elif type == 'ICMP':
#         print(' '.join([snifftime, 'ICMP'.rjust(4, ' '),  str(pkt.getlayer(IP).src).rjust(15, ' ') , ('t: '+ str(pkt.getlayer(ICMP).type)).rjust(5, ' '), '-->' , str(pkt.getlayer(IP).dst).rjust(15, ' '), ('c: ' + str(pkt.getlayer(ICMP).code)).rjust(5, ' ')]))

#     else:
#         pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PCAP reader')
    parser.add_argument('--pcap', metavar='<pcap file name>',
                        help='pcap file to parse', required=True)
            
    args = parser.parse_args()
    
    file_name = args.pcap
    if not os.path.isfile(file_name):
        print('"{}" does not exist'.format(file_name))
        sys.exit(-1)
    read_pcap(file_name)

   
    sys.exit(0)

