from device_security_scanner import *
import scapy.all as scapy
import boto3
import os
import time

class ArrayHandler(logging.Handler):
	def emit(self, record):
		log_array.append(record.getMessage())

logging.basicConfig(level=logging.INFO)
log_array = []
logger = logging.getLogger()
logger.addHandler(ArrayHandler())

class s3():
	def __init__(self):
		self.bucket = 'thingscopeminibucket'
		self.s3Client = boto3.client('s3')

	def get(self, key):
		path = f"/tmp/{key}"
		self.s3Client.download_file(self.bucket, key, path)
		return path

	def put(self, key, file, type):
		self.s3Client.put_object(Bucket = self.bucket, Key=key, Body=file, ContentDisposition='inline', ContentType=type)

def handler(event, context):
	key = event['Records'][0]['s3']['object']['key'] 
	if key.split('.')[-1] == 'pcap':
		pcap_file = s3().get(key)
		packets = scapy.rdpcap(pcap_file)
		unique_macs = list(set([x.src for x in packets]))
		for mac in unique_macs:
			logging.info(f"Now processing {mac}\n\n")
			security_analyzer = SecurityAnalyzer(device_mac_address=mac, internal_ip_prefix= ["10.","192."])
			for pkt in packets:
				security_analyzer.pktHandler(pkt)
			security_analyzer.postProcess()
			security_analyzer.printStore()

		filename = f"report_{key.split('.')[:-1][0]}.txt"
		s3().put(filename, '\n'.join(log_array), 'txt')

if __name__ == "__main__":
	handler({"Records": [{"s3": {"object": {"key": "etekcity_2_16.pcap"}}}]}, None)