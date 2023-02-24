# IoT Device Endpoints & Security Analyzer Tool

## Setup

```buildoutcfg
> git clone https://github.com/pankajtakawale/iot-security.git
> virtualenv venv
> source venv/bin/activate
> pip install -r requirements.txt
```

## Usage

```
> python device_security_scanner.py
usage: device_security_scanner.py [-h] [--pcap PCAP] [--db_url DB_URL] [--title TITLE] [--save_pcap] [--disable_sink] (--devmacaddr DEVMACADDR | --iface IFACE)
                                  [--sink_interval SINK_INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  --pcap PCAP           pcap file to process
  --db_url DB_URL       Enter DB Connection Endpoint
  --title TITLE         Device Title to save. Useful when you are processing single pcap file. Otherwise, you will have to update device title through Web UI
  --save_pcap           Enable Pcap file saving to create pcap file. Useful when processing live network traffic.
  --disable_sink        Disable Sink. This will just print final Device Endpoint map.
  --devmacaddr DEVMACADDR
                        MAC address of IoT device if you want to process only single IoT Device from pacap file
  --iface IFACE         Interface to listen
  --sink_interval SINK_INTERVAL
                        Sink Interval in seconds. While processing live network stream, how often do you want to update database
```
### Examples

#### Processing Single pcap file, process single Mac Address from pcap file, Do Not save to database
```
> python device_security_scanner.py --devmacaddr="10:27:f5:8a:7b:de" --pcap=/Users/pankaj/cvn/IoT-ren/training_pcaps/tclink.pcap --disable_sink
```

#### Save in a different database
```
> python device_security_scanner.py --devmacaddr="10:27:f5:8a:7b:de" --pcap=/home/pankaj/iot/training_pcaps/tclink.pcap --title=TPLinkSwitch --db_name=iottest

--devmacaddr="ec:2b:eb:47:a1:56" --pcap=/home/pankaj/iot/iot-security/pcap_database/echo19.pcap --disable_sink

```

#### Listen on WiFi HotSpot Interface

```
> ip address show

capture WiFI hotspot interface, say wlp0s20f3

> python device_security_scanner.py --iface=wlp0s20f3 --db_name=iotv2 --save_pcap --iface_mac_addr=0c:9a:3c:4e:ba:dd

```

### Domain IP Monitor

```
python domain_ip_monitor.py  --interval=10 --times=10 --db_name=iotv2 --device_macs="10:27:f5:8a:7b:de,ec:2b:eb:47:a1:56,18:b7:9e:02:3d:90,80:9f:9b:f6:4a:c7,e4:26:86:f2:ef:b7,dc:4f:22:8d:9b:7a,10:52:1c:42:15:b2,8c:85:80:3a:4e:4f,78:11:dc:21:9a:f9,b4:c9:b9:92:89:fc,90:20:3a:07:b4:48,a4:da:22:2f:6f:6a,38:01:46:8b:d3:46,10:09:f9:1e:c7:c7,90:0c:c8:fb:34:ef"

```

