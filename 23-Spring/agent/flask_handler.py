from flask import Flask
from device_security_scanner import *
import json

app = Flask(__name__)

@app.route("/agent")
def agent():
    try:
        pcap_path = request.args.get('path')
        report = json.dumps(process_pcap(pcap_path), sort_keys=True)
        filename = f"report_{pcap_file.split('.')[:-1][0]}.json"
        with open(filename, 'w') as f:
            f.write(report)
        return '200 OK', 200
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500
