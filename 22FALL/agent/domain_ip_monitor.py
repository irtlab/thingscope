import subprocess
import sys
import argparse
import datetime
import time
import pandas as pd
import numpy as np
import numpy as np
import pandas as pd
from sink import DeviceSink


def process_domain(domain):
    domain = domain.strip()
    process = subprocess.Popen(['dig', '+short', domain],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    ip_set = set()
    while True:
        output = process.stdout.readline()
        ol = output.strip()
        if ol != "": ip_set.add(ol)
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                ol = output.strip()
                if ol != "": ip_set.add(ol)
            break

    ip_list = list(ip_set)
    ip_list.sort()
    #ips = ','.join(ip_list)
    return ip_list


def get_domain_names(eps):
    domain_set = set()
    for ep in eps:
        domain = ep.get('domain_name')
        if not domain or domain == "":
            continue
        domain_set.add(domain)
    return list(domain_set)

def perform_dns_ip_mapping(sink, device, interval, n):

    df = pd.DataFrame(columns=['datetime', 'domain', 'ips', 'device_mac'])

    for i in range(n):
        print('-----------------------------------------------')
        print(f'Starting iteration {i}')
        now = datetime.datetime.now()
        for device in device_macs:
            print(f'Processing device {device}')
            eps = sink.fetch_endpoints({'device_mac' : device})
            domains = get_domain_names(eps)
            for domain in domains:
                try:
                    if not domain:
                        continue
                    domain = domain.strip()
                    if domain == "":
                        continue
                    ips = process_domain(domain)
                    sink.update_domain_ips(device, domain, ips)
                    df = pd.concat([df, pd.DataFrame.from_records([{'domain': domain, 'ips': ips, 'device_macs':device, 'datetime': now.strftime("%m/%d/%Y, %H:%M:%S")}])])
                    print(f'{now} device {device} domain {domain} ips {ips}')
                except Exception as e:
                    print('error processing')
        time.sleep(interval)

    #print(df.groupby('domain')['ips'].nunique())
    g = df.groupby('domain')['ips'].apply(lambda x: np.unique(x))
    df = g.reset_index()
    def make_flat(input_list):
        flat = [element for nestedlist in input_list for element in nestedlist]
        flats = set(flat)
        return list(flat)


    df['ipsf'] = df.apply(lambda row: make_flat(row['ips']), axis=1)
    df['num_ips'] = df.apply(lambda row: len(row['ipsf']), axis=1)
    df = df.drop(['ips'], axis=1)
    print(df.to_markdown())


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--db_name", help="DB Name", default="iottest")
    parser.add_argument("--device_macs", help="Comma separated Device Macs", default="10:27:f5:8a:7b:de")
    parser.add_argument("--interval", help="Interval in Seconds", default="10")
    parser.add_argument("--times", help="", default="5")

    args = parser.parse_args()

    sink = DeviceSink(db_name=args.db_name)

    device_macs = args.device_macs.split(',')

    perform_dns_ip_mapping(sink, device_macs, int(args.interval), int(args.times))
