import kyd
import dpkt
import requests
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
import os 
from fingerbank_key import *
cwd = os.getcwd()


## Return Finger Bank Device name ##

def DHCP_profile(pcap):
    # Get DHCP fingerprint from kyd.py
    dhcp_fingerprint = []
    with open(pcap, 'rb') as fp:
        try:
            capture = dpkt.pcap.Reader(fp)
        except ValueError as e:
            raise Exception("File doesn't appear to be a PCAP: %s" % e)
        output = kyd.process_pcap(capture)
        for record in output:
            dhcp_fingerprint.append(record['DHCPFP'])
    # Query fingerbank api to get decive name
    if (len(dhcp_fingerprint)>0):
        print("***** Finger Bank Device name : ",query_fingerbank(dhcp_fingerprint[0]),"  *****")
    else:
        print("No DHCP fingerprint")


## Query FingerBank API and return device name ##
def query_fingerbank(fingerPrint):
    headers = {'Content-Type': 'application/json'}
    url = 'https://api.fingerbank.org/api/v2/combinations/interrogate?key='\
           + fingerbank_key_val
    params = {'dhcp_fingerprint' : fingerPrint }
    resp = requests.get(url, headers = headers, params=params)
    info = resp.json()
    try:
        err = info['errors']
        print(err)
        return "", ""
    except KeyError:
        device_name = info['device_name']
        t = device_name.split('/', 1)[0]
        return t, info['device']['name'] 

## Return Domain name (DNS)
def domain_name(pcap):
    pcap_path = cwd +"/"+  pcap
    dns_packets = rdpcap(pcap_path)
    dst = []
    dname = []
    for packet in dns_packets:
        if packet.haslayer(DNS):
            dst.append(packet[IP].dst)
            dname.append(packet[DNSQR].qname)
    if (len(dname)>0):
        print("***** Domain name (DNS): ", dname[0] , "  *****")
    else:
        print("No Domain Name ")
    



