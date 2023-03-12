from device_security_scanner import *
from analysis4 import *
import boto3
import logging
import time
from apiclient.discovery import build
from google.oauth2.service_account import Credentials
from apiclient.http import MediaFileUpload
import json

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

class google():
	def __init__(self):
		secret_name = "thingscopegoogle"
		region_name = "us-east-1"
		session = boto3.session.Session()
		client = session.client(service_name='secretsmanager',region_name=region_name)
		get_secret_value_response = client.get_secret_value(SecretId=secret_name)
		creds = json.loads(get_secret_value_response['SecretString'])["thingscopegoogle"]
		credentials = Credentials.from_service_account_info(creds)
		self.drive = build('drive', 'v3', credentials=credentials)


	def push(self, filename, file):
		filepath = f"/tmp/{filename}"
		with open(filepath, 'w') as f:
			f.write(file)
		file_metadata = {'name': filename,'mimeType': 'text/plain', 'parents': ['1A0ScUpFS6B9nbOxGo0GlSuHwjRpDx060']}
		media = MediaFileUpload(mimetype='text/plain', filename=filepath)
		file = self.drive.files().create(body=file_metadata, media_body=media).execute()

	def get(self, key):
		filename = self.drive.files().get(fileId=key).execute()['name']
		path = f"/tmp/{filename}"
		file = self.drive.files().get_media(fileId=key).execute()
		with open(path, 'wb') as f:
			f.write(file)
		return filename

def main(pcap_file):
	report = json.dumps(process_pcap(f"/tmp/{pcap_file}"), sort_keys=True)
	filename = f"report_{pcap_file.split('.')[:-1][0]}.json"
	return report

def beta(pcap_file):
	report = json.dumps(betaMain(f"/tmp/{pcap_file}"), sort_keys=True)
	return report

def handlerFromS3(event, context):
	key = event['Records'][0]['s3']['object']['key']
	if key.split('.')[-1] == 'pcap':
		pcap_file = s3().get(key)
		x = main(pcap_file)

def handlerFromDrive(event, context):
	filename = google().get(event['queryStringParameters']['id'])
	noDrop = 'noDrop' in event['queryStringParameters']
	isBeta = 'beta' in event['queryStringParameters']
	if isBeta:
		report = beta(filename)
	else:
		report = main(filename)
	if not noDrop:
		s3().put(filename, report)
		google().push(filename, report)
	return {"statusCode": "200", "headers": {"Content-Type": "application/json",},"body": report}