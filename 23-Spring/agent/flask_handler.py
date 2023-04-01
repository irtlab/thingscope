from flask import Flask, request
from device_security_scanner import *
from aws_handler import *
import json
import os

app = Flask(__name__)

# This is the endpoint that the agent will call to transform the pcap file into the endpoint report
# The saved file should be in the attached volume in the docker compose file
@app.route("/agent")
def agent():
    try:
        pcap_path = request.args.get('path')
        report = json.dumps(process_pcap(f"pcap/{pcap_path}"), sort_keys=True)
        filename = f"report_{pcap_path.split('.')[:-1][0]}.json"
        with open(f"analysis/{filename}", 'w') as f:
            f.write(report)
        # returns the json output to the browser
        return report, 200
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500
    
@app.route("/agent/legacy")
def agentLegacy():
    return handlerFromDrive({'queryStringParameters' : {'id': request.args.get('id')}}, None)
    try:
        return handlerFromDrive({'queryStringParameters' : {'id': request.args.get('id')}}, None)
    except Exception as e:
        return str(e), 500

# Uploads a file to the volume. Posts the file in the HTTP request
@app.route("/upload_pcap", methods=['POST'])
def upload():
    try:
        if request.method == 'POST':
            f = request.files['file']
            f.save(f"pcap/{f.filename}")
            return '200 OK', 200
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# List all files in the volume
@app.route("/list_pcap")
def list_pcap():
    try:
        files = os.listdir("pcap")
        return str(files), 200
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

@app.route("/list_analysis")
def list_analysis():
    try:
        files = os.listdir("analysis")
        return str(files), 200
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500
    
# return hello world at root
@app.route("/")
def hello():
    return "Hello World!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)