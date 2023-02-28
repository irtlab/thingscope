from device_security_scanner import *
import boto3
import logging
import time
from apiclient.discovery import build
from google.oauth2.service_account import Credentials
from apiclient.http import MediaFileUpload
import json

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

def googlePush(filename, file):
	filepath = f"/tmp/{filename}"
	with open(filepath, 'w') as f:
		f.write(file)
	secret_name = "thingscopegoogle"
	region_name = "us-east-1"

	session = boto3.session.Session()
	client = session.client(service_name='secretsmanager',region_name=region_name)
	get_secret_value_response = client.get_secret_value(SecretId=secret_name)
	creds = json.loads(get_secret_value_response['SecretString'])["thingscopegoogle"]

	credentials = Credentials.from_service_account_info(creds)
	drive = build('drive', 'v3', credentials=credentials)
	file_metadata = {'name': filename,'mimeType': 'text/plain', 'parents': ['1A0ScUpFS6B9nbOxGo0GlSuHwjRpDx060']}
	media = MediaFileUpload(mimetype='text/plain', filename=filepath)

	file = drive.files().create(body=file_metadata, media_body=media).execute()

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
		process_pcap(pcap_file, ["10.", "192.168.", "253.", "254.", "255."])
		filename = f"report_{key.split('.')[:-1][0]}.txt"
		s3().put(filename, '\n'.join(log_array))
		googlePush(filename, '\n'.join(log_array))