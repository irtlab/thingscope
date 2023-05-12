from flask import Flask, request
from device_security_scanner import *
from aws_handler import *
import json
import os
from sink import *
from compare import *
import pandas

app = Flask(__name__)

# This is the endpoint that the agent will call to transform the pcap file into the endpoint report
# The saved file should be in the attached volume in the docker compose file
@app.route("/agent")
def agent():
    try:
        path = request.args.get('path')
        title = request.args.get('title')
        process_pcap_sink(f"../data/files/{path}", title, os.environ['ATLAS_URI'], os.environ['IOT_DB_NAME'])
        return 'Sucess', 200
    except Exception as e:
         print(e)
         return 'Internal Server Error', 500
    
@app.route("/agent/legacy")
def agentLegacy():
   try:
       path = request.args.get('path')
       return process_pcap_interactive(f"../data/files/{path}")
   except Exception as e:
        print(e)
        return 'Internal Server Error', 500


@app.route("/agent/drive")
def agentDrive():
    try:
        return handlerFromDrive({'queryStringParameters' : {'id': request.args.get('id')}}, None)
    except Exception as e:
        return str(e), 500

@app.route("/agent/compare")
def compare():
    #try:
        old = request.args.get('old')
        new = request.args.get('new')
        comparison = compareEndpoints(old, new, os.environ['ATLAS_URI'], os.environ['IOT_DB_NAME'])
        df  = pandas.DataFrame()
        for key, value in comparison.items():
            if key != 'Differences':
                for subkey, subvalue in value.items():
                    df.loc[key, subkey] = '\\n'.join(subvalue)
        return df.to_html().replace("\\n","<br>"), 200
    #except Exception as e:
    #    return str(e), 500

# Uploads a file to the volume. Posts the file in the HTTP request
@app.route("/agent/upload_pcap", methods=['POST'])
def upload():
    try:
        f = request.files['file']
        f.save(f"pcap/{f.filename}")
        return '200 OK', 200
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500

# List all files in the volume
@app.route("/agent/list_pcap")
def list_pcap():
    #try:
    files = os.listdir("pcap")
    return '<br>'.join(files), 200
    # except Exception as e:
    #     print(e)
    #     return 'Internal Server Error', 500

@app.route("/agent/db/endpoints")
def output_db_endpoints():
    db = DeviceSink(db_url=os.environ['ATLAS_URI'], db_name=os.environ['IOT_DB_NAME'])
    endpoints = [x for x in db.endpoints_coll.find()]
    return endpoints, 200

@app.route("/agent/db/devices")
def output_db_devices():
    db = DeviceSink(db_url=os.environ['ATLAS_URI'], db_name=os.environ['IOT_DB_NAME'])
    devices = [x for x in db.devices_coll.find()]
    for device in devices:
        device['_id'] = str(device['_id'])
    return devices, 200

@app.route("/agent/db/domains")
def output_db_domains():
    db = DeviceSink(db_url=os.environ['ATLAS_URI'], db_name=os.environ['IOT_DB_NAME'])
    domains = [x for x in db.domain_coll.find()]
    for domain in domains:
        domain['_id'] = str(domain['_id'])
    return domains, 200

# given a name, return all endpoints with that name in {}
@app.route("/agent/db/endpoints/<name>")
def output_db_endpoints_name(name):
    db = DeviceSink(db_url=os.environ['ATLAS_URI'], db_name=os.environ['IOT_DB_NAME'])
    endpoints = [x for x in db.endpoints_coll.find({'_id.name': name})]
    return endpoints, 200

# given a name, return all devices with that name in {}
@app.route("/agent/db/domains/<name>")
def output_db_devices_name(name):
    db = DeviceSink(db_url=os.environ['ATLAS_URI'], db_name=os.environ['IOT_DB_NAME'])
    devices = [x for x in db.domain_coll.find({'_id.name': name})]
    return devices, 200

# return hello world at root
@app.route("/")
def hello():
    return "Hello World!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)