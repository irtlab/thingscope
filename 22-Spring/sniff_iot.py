'''
authors: Lama Rashed , Xiaoqi Lin 
Data : June 6, 2021

 1- Capture specific device traffic ( by ip address, in future we will add the ability to filter by MAC address as well)
 2- Save PCAP file
 3- Obtain and Print device name from FingerBank API "if any"
 4- Obtain and Print device manufacturer's name using DNS services   
 5- Convert PCAP file into flow file using Tranalyzer
 6- Import the final feature vector obtained previously ( after doing feature selection methods ) 
 7- Import trained machine learning models
 8- Predict the flow file using the ML models.
 
'''
from scapy.all import *
import sys
import argparse
from t2py import T2Utils
import tranalyzer
import dhcp_dns
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--devid", help="Enter IP address of the device", default="example")
    args = parser.parse_args()
    args = vars(parser.parse_args())
    dev_id = args["devid"]


    try: 
        filter = "ip src "+dev_id+""
        # Capture/sniff traffic of an IoT device for 30 mintues and filter by its IP address 
        capture = sniff(filter=filter, timeout=1800,  iface="en0")
        name = dev_id + ".pcap"
        # Save captured traffic to PCAP files
        wrpcap(name,capture)
        # Get device information from FingerBank API
        dhcp_dns.DHCP_profile(name)
        # Use DNS services to retrieve the name of the manufacturer
        dhcp_dns.domain_name(name)
        # Convert pcap file into flow file using Tranalyzer
        tranalyzer.convert_pcap(name)
    except Exception as e:
        print("[ERROR] Sniffer File: " + e)
