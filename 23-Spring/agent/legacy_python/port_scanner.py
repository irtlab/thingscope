import nmap
from sink import DeviceSink

def get_open_ports(ip):
    nmScan = nmap.PortScanner()
    res = nmScan.scan(ip, '0-65535')
    print(res)
    print(nmScan.scaninfo())

    open_ports = set()
    for host in nmScan.all_hosts():
        print('Host : %s (%s)' % (host, nmScan[host].hostname()))
        print('State : %s' % nmScan[host].state())
        print(f'nmScan : {nmScan[host]}')

        for proto in nmScan[host].all_protocols():
            print('----------')
            print('Protocol : %s' % proto)

            lport = nmScan[host][proto].keys()
            for port in lport:
                print('port : %s\tstate : %s' % (port, nmScan[host][proto][port]['state']))
                if nmScan[host][proto][port]['state'] == 'open':
                    open_ports.add(port)

    opl = list(open_ports)
    opl.sort
    open_port_val = ','.join(map(str, opl))
    return open_port_val


ip = '10.42.0.122'
ops = get_open_ports(ip)
sink = DeviceSink(db_name='iotv2')
print(f'open ports for {ip} = {ops}')
sink.update_open_ports(ip, ops)
