from device_security_scanner import *
import boto3
import logging
import time

class ArrayHandler(logging.Handler):
	def emit(self, record):
		log_array.append(record.getMessage())

class s3():
	def __init__(self):
		self.bucket = 'thingscopeminibucket'
		self.s3Client = boto3.client('s3')

	def get(self, key):
		path = f"/tmp/{key}"
		self.s3Client.download_file(self.bucket, key, path)
		return path

	def put(self, key, file):
		self.s3Client.put_object(Bucket = self.bucket, Key=key, Body=file, ContentDisposition='inline')

def handler(event, context):
	time.sleep(30)
	global log_array
	log_array = []
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	logger.addHandler(ArrayHandler())
	key = event['Records'][0]['s3']['object']['key'] 
	if key.split('.')[-1] == 'pcap':
		pcap_file = s3().get(key)
		process_pcap(pcap_file, ['10.', '192.168.'])
		filename = f"report_{key.split('.')[:-1][0]}.txt"
		s3().put(filename, '\n'.join(log_array))