# iot-devices-database

The IoT Devices dataset represents the traffic emitted during the setup of **15 smart home IoT devices**.

The data is available to download from Google Drive [location](https://drive.google.com/drive/folders/1h44A_70NIUPESQeik_O9H8BcE6yaBvC7)

Each sub-directory represents the IoT device named as device's mac address. 

```
ec:2b:eb:47:a1:56.pcap  Captured network traffic for a device
devicemeta.json         Device Meta data
domainips.json          Domain to IP mapping and count for the device's remote endpoints
endpoints.json          List of remote endpoints device communicated with and its details

```


### endpoints.json

```
{
  "_id": "52.46.133.19",
  "port": "443/tcp",
  "protocol": "https",
  "ip": "52.46.133.19",
  "security_posture": "encrypted",
  "domain_name": "todo-ta-g7g.amazon.com",
  "self_signed": false,
  "cert_details": [
    "SSL connection using TLSv1.2 / ECDHE-RSA-AES128-GCM-SHA256",
    " subject: CN=todo-ta-g7g.amazon.com",
    " start date: Oct 19 00:00:00 2022 GMT",
    " expire date: Oct 18 23:59:59 2023 GMT",
    " subjectAltName: host \"todo-ta-g7g.amazon.com\" matched cert\\'s \"todo-ta-g7g.amazon.com\"",
    " issuer: C=US; O=DigiCert Inc; CN=DigiCert Global CA G2"
  ],
  "location": {
    "city": "Ashburn",
    "region": "Virginia",
    "country": "United States",
    "org": "AMAZON-02",
    "version": "IPv4",
    "latitude": 39.017388,
    "longitude": -77.468037
  },
  "device_mac": "ec:2b:eb:47:a1:56",
  "auth_algorithm": "RSA",
  "cert_tls_version": "TLS1.2",
  "enc_algorithm": "AES 128 GCM",
  "gnutls_name": "TLS_ECDHE_RSA_AES_128_GCM_SHA256",
  "hash_algorithm": "SHA256",
  "hex_byte_1": "0xC0",
  "hex_byte_2": "0x2F",
  "kex_algorithm": "ECDHE",
  "openssl_name": "ECDHE-RSA-AES128-GCM-SHA256",
  "protocol_version": "TLS",
  "security": "secure"
}
```

### devicemeta.json

```
{
  "_id": "ec:2b:eb:47:a1:56",
  "ip": "10.42.0.179",
  "name": "AmazonAlexa",
  "mac_addr": "ec:2b:eb:47:a1:56",
  "mfgr": "Amazon",
  "device_type": "SmartHome",
  "device_tag": "TBD",
  "enabled": true,
  "device": null,
  "open_ports": "4070,8888,55442,55443,1080"
}
```

### domainips.json

```
{
  "_id": {
    "$oid": "63a489e2486c1081071170be"
  },
  "device_mac": "ec:2b:eb:47:a1:56",
  "domain_name": "ec2.web.me-south-1.prod.diagnostic.networking.aws.dev",
  "ip_count": 3,
  "ips": "15.184.245.166,157.175.241.61,157.241.5.46"
}
```
