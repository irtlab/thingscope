from scapy.all import *

from fingerbank_key import *
import requests

def query_fingerbank(req_list, option):
    headers = {'Content-Type': 'application/json'}
    url = 'https://api.fingerbank.org/api/v2/combinations/interrogate?key='\
           + fingerbank_key_val
    str1 = ','.join(str(e) for e in req_list)
    # params = {'dhcp_fingerprint': str1 }

    if option == 55:
        params = {'dhcp_fingerprint': str1 }
    elif option == 60:
        params = {'dhcp_vendor': req_list}

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

def hex_mac(chaddr):
    # converts mac address to required text format for readabiliy and signatures
    MAC = ""
    for b in str(chaddr):
        digit = hex(ord(b))
        digit = digit.split('x', 1)[1]
        if(len(digit)==1):
            MAC += "0"
        MAC += digit
        MAC += ":"
    return MAC[ : 17]

def get_device_dhcp_info(pkt):

    features = {'mac_address': "", 'manufacturer':"", 'os': "",\
            'device_type': "", 'IoT': True}
    req_list = []

    try:
        features['mac_address'] = hex_mac(pkt[BOOTP].chaddr)
    except Exception as e:
        print e

    #if features['mac_address'] != pkt.src:
    #    print('Src mac address mismatches with DHCP messages')
    
    try:
        options = pkt[BOOTP][DHCP].options
    except Exception as e:
        try:
            options = pkt['BOOTP']['DHCP'].options
        except Exception as e:
            raise e
    for option in options:
        if type(option) is tuple:
            opt_name = option[0]
            opt_value = option[1]
            if opt_name == 'param_req_list':
                #for b in str(opt_value):
                #    req_list.append(ord(b))
                t, v = query_fingerbank(opt_value, 55)
                if t == "Operating System":
                    features['os'] = v
                    if (v.find('Apple OS') != -1) or (v.find('Windows OS') != -1):
                        features['IoT']= False
                    print("[INFO] " + v + " detected from DHCP option 55")
                else :
                    if t != "":
                        print("[INFO] " + v + " detected from DHCP option 55")
                        features['device_type'] = v
                        if (v.find('Printer') != -1):
                            features['IoT'] = True
            if opt_name == 'vendor_class_id':
                v_id = opt_value.decode('ascii')
                t, v = query_fingerbank(v_id, 60)
                if t == "Operating System":
                    features['os'] = v
                    if (v.find('Apple OS') != -1) or (v.find('Windows OS') != -1):
                        features['IoT']= False
                    print("[INFO] " + v + " detected from DHCP option 60")
                else:
                    if t != "":
                        print("[INFO] " + v + " detected from DHCP option 60")
                        features['device_type'] = v
                        if (v.find('Printer') != -1):
                            features['IoT'] = True

    return features
