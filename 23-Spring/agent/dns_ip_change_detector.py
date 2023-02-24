import subprocess
import sys
import argparse
import datetime
import time
import pandas as pd
import numpy as np
import numpy as np
import pandas as pd


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

def perform_dns_ip_mapping(domain_file, interval, n):
    domains = open(domain_file, 'r')
    domain_lines = domains.readlines()

    df = pd.DataFrame(columns=['datetime', 'domain', 'ips'])

    for i in range(n):
        now = datetime.datetime.now()
        for domain in domain_lines:
            domain = domain.strip()
            if domain == "":
                continue
            ips = process_domain(domain)
            df = pd.concat([df, pd.DataFrame.from_records([{'domain': domain, 'ips': ips, 'datetime': now.strftime("%m/%d/%Y, %H:%M:%S")}])])
            logging.debug(f'{now} domain {domain} ips {ips}')
        time.sleep(interval)

    #logging.debug(df.groupby('domain')['ips'].nunique())
    g = df.groupby('domain')['ips'].apply(lambda x: np.unique(x))
    df = g.reset_index()
    def make_flat(input_list):
        flat = [element for nestedlist in input_list for element in nestedlist]
        flats = set(flat)
        return list(flat)


    df['ipsf'] = df.apply(lambda row: make_flat(row['ips']), axis=1)
    df['num_ips'] = df.apply(lambda row: len(row['ipsf']), axis=1)
    df = df.drop(['ips'], axis=1)
    logging.debug(df.to_markdown())


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--domains_file", help="Domain list file", default="")
    parser.add_argument("--interval", help="Interval in Seconds", default="30")
    parser.add_argument("--times", help="", default="5")

    args = parser.parse_args()

    perform_dns_ip_mapping(args.domains_file, int(args.interval), int(args.times))
