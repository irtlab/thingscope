# compare the IPs in endpoints.json to the IPs in mongodb
import json
import os
from agent.sink import *
import ipaddress

# os.walk the pankaj/data folder. For each folder, the name of the device is the name of the folder and the ips are the endpoints.json file inside that folder
sink = DeviceSink()

for root, dirs, files in os.walk("../../pankaj/data"):
    for name in dirs:
        deviceName = name.replace("_", ":")
        print(deviceName)
        with open(os.path.join(root, name, "endpoints.json")) as f:
            data = json.load(f)
            for endpoint in data:
                anyFound = False
                ip = endpoint['ip']
                if ipaddress.ip_address(ip).is_private:
                    continue
                # check if the ip exists in the mongodb
                # if it does, then check if the ip is in the same device
                tempEndpoints = [x for x in sink.endpoints_coll.find({'ip': ip, 'device_mac': deviceName})]
                if tempEndpoints:
                    pass
                    #print(f"\t{ip} exists in {deviceName}")
                else:
                    anyFound = True
                    print(f"\t{ip} does not exist in {deviceName}")
            if not anyFound:
                print(f"\tAll endpoints exist in mongodb")