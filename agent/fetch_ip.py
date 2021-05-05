#!/usr/bin/env python

import sys
import json
import socket
import os
from subprocess import Popen, PIPE, call
import sqlite3
import dns.resolver


def implementIPTablesByJson(file, mac_addr):
    #obtain desired MUD-like object to parse.
    #verify and obtain if file content is JSON format
    try:
        json_object = json.loads(file)

    except ValueError:
        print("Incorrect File Content Format: JSON")
        sys.exit()

    print("Parsing ACL from Mud Profile")
    #parse mud-like json for ACL
    ACL_array = json_object["ietf-access-control-list:access-lists"]["acl"]


    ACLtoIPTable(ACL_array, mac_addr)

def dst_or_src_dnsname(matches):
    if "ietf-acldns:src-dnsname" in matches["ipv4"]:
        return ["ietf-acldns:src-dnsname", "source-port"]
    elif "ietf-acldns:dst-dnsname" in matches["ipv4"]:
        return ["ietf-acldns:dst-dnsname", "destination-port"]

def get_prot(matches, dnsName):
    if("tcp" in matches):
        subport = matches["tcp"]
        prot = "tcp"
    elif("udp" in matches):
        subport = matches["udp"]
        prot = "udp"
    else:
        print("Error in Matches")
        return

    # subport["source-port"]["port"] 
    # or 
    # subport["destination-port"]["port"]
    dport = str(subport[dnsName]["port"])
    return prot, dport

def get_destName(matches, dnsName):
    return matches["ipv4"][dnsName]

def get_dest_ip(dstName):
    A = dns.resolver.query(dstName, 'A')

    res = []
    for i in A.response.answer:
        for j in i.items:
            if j.rdtype == 1:
                destIp = j.address
                res.append(destIp)
                for c in destIp:
                    if c.isalpha():
                        res.remove(destIp)
                        break
    return res

def parse_info(matches, mac_addr):
    # get dst or src
    # pre-process
    dnsName = dst_or_src_dnsname(matches)
    # get protocol and dst port
    prot, dport = get_prot(matches, dnsName[1])
    # get dst Ip list
    dstName = get_destName(matches, dnsName[0])
    dstIpList = get_dest_ip(dstName)

    try:
        hostName = get_hostname(mac_addr.replace(":","-") + ".pcap")
    except Exception as e:
        print "[ERROR] Error at fetch_ip.py line 83, unable to get hostName" + e.message
        print "Set hostName = cannot-find-name"
        hostName = "cannot-find-name"

    return prot, dport, dstIpList, dstName, hostName

def check_SQL_table():
    #configure database and connect
    #check if device database exist
    exists = os.path.exists('device.db')

    if not exists:
        #create db and insert main schema
        conn = sqlite3.connect('device.db')
        print("Database has been created")
        conn.execute('CREATE TABLE DEVICE (NAME CHAR(20) NOT NULL, HOSTNAME CHAR(20) NOT NULL, DOMAIN CHAR(50) NOT NULL, IP CHAR(20) NOT NULL, PORT CHAR(20) NOT NULL, PROTOCOL CHAR(20) NOT NULL);')
        print("Main device table created")
        conn.commit() 

def has_dup(cursor, mac_addr, dstName):
    query = "select NAME, DOMAIN, IP, PORT, PROTOCOL from DEVICE WHERE NAME = ? and DOMAIN = ?"
    try:
        res = cursor.execute(query, [mac_addr, dstName])
    except Exception as e:
        print e
    size = len(res.fetchall())
    # size != 0, has dup, return true
    return size != 0

def ACLtoIPTable(acl, mac_addr):

    # open database
    check_SQL_table()
    conn = sqlite3.connect('device.db')
    print("Database is running")
    cursor = conn.cursor()

    try:
        ace = acl[0]["aces"]['ace']
        for index in ace:
            matches = index["matches"]

            #Confirm that matches has valid info for dest addr
            if("ietf-acldns:src-dnsname" not in matches["ipv4"] and \
            "ietf-acldns:dst-dnsname" not in matches["ipv4"]):
                continue

            try:
                # get ACCEPT or REJECT
                target = index["actions"]["forwarding"].upper()
            except Exception as e:
                print "[ERROR] Some MUD file format includes actions inside matches."
                print e

            try:
                prot, dport, dstIpList, dstName, hostName = parse_info(matches, mac_addr)
            except Exception as e:
                print "[ERROR] Error at parse_info"
                print e

            # for each dst IP
            print("*********" + dstName + "*************")
            if not has_dup(cursor, mac_addr, dstName):
                for dstIp in dstIpList:
                    call('iptables -A FORWARD -p ' + prot + ' -d ' + dstIp + ' --dport ' + dport + ' -m mac --mac-source ' + mac_addr + ' -j ' + target + '', shell=True)
                    print("[INFO] Implemented rule for: source-> " + mac_addr + " dest-> " + dstIp)
                    print ""
                    try:
                        query = "INSERT INTO DEVICE(NAME, HOSTNAME, DOMAIN, IP, PORT, PROTOCOL) VALUES(?,?,?,?,?,?)"
                        cursor.execute(query, (mac_addr, hostName, dstName, dstIp, dport, prot))
                        conn.commit()
                    except Exception as e:
                        print e
            else:
                print("[INFO] Rules exist for source-> " + mac_addr + " dest-> " + dstName)
            print("**********************")
    except Exception as e:
        print "Some MUD Files use \'ace\' and some use \'aces\'"
        print "Check mud file format"
        print e
    
    #call ('iptables -I FORWARD -d 17.142.160.59 -j DROP', shell=True)
    call('iptables -A FORWARD -m mac --mac-source ' + mac_addr + ' -j DROP' + '', shell=True)
    conn.close()




def get_hostname(pcap_file):
    import dpkt
    with open(pcap_file) as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            udp = ip.data
            dhcp = dpkt.dhcp.DHCP(udp.data)

            for opt in dhcp.opts:
                if opt[0] == 12:
                    print opt[1]
                    return opt[1]
    return 'cannot-find-name'