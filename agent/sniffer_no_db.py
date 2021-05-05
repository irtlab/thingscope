from scapy.all import *
from new_dns_callback import DNSCallback
import sys
import argparse
from colorprint import ColorPrint as color

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--devname", help="Enter the name of the device", default="example")
    parser.add_argument("--devmodel", help="Enter the model of the device", default="example")
    parser.add_argument("--manuname", help="Enter the name of the manufacturer", default="example")
    parser.add_argument("--manuweb", help="Enter the website of the manufacturer", default="http://example.com")
    parser.add_argument("--ignore", help="Enter MAC address of device to ignore", default="")
    args = parser.parse_args()
    
    print(color.OKBLUE + "[INFO] Observing Network Traffic" + color.ENDC)
    
    dns_callback = DNSCallback(device_name=args.devname, device_model=args.devmodel, manufacturer_name=args.manuname, manufacturer_website=args.manuweb, ignore_device=args.ignore)
    
    # Add router MAC to list of devices seen
    # router_mac =  sys.argv[1]
    # dns_callback.add_to_ignore_device_list(router_mac)
    
    try:
        sniff(prn=dns_callback.pktHandler, iface="wlan0")
    except Exception as e:
        print(color.ERROR + "[ERROR] Sniffer File: " + e + color.ENDC)