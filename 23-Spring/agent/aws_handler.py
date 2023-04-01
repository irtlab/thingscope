from device_security_scanner import *
import boto3
from apiclient.discovery import build
from google.oauth2.service_account import Credentials
from apiclient.http import MediaFileUpload
import json

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

def handlerFromDrive(event, context):
	filename = google().get(event['queryStringParameters']['id'])
	newFilename = f"report_{filename.split('.')[:-1][0]}.json"
	noDrop = 'noDrop' in event['queryStringParameters']
	isBeta = 'beta' in event['queryStringParameters']
	if isBeta:
		report = beta(filename)
	else:
		report = main(filename)
	if not noDrop:
		google().push(newFilename, report)
	return {"statusCode": "200", "headers": {"Content-Type": "application/json",},"body": report}