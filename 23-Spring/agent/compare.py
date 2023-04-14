import json
from sink import *

def compareEndpoints(old, new, db_url, db_name):
    sink = DeviceSink(db_url, db_name)
    devices = sink.devices_coll.find()
    if not [x for x in devices if x['_id'] == old] and not [x for x in devices if x['_id'] == new]:
        return "Device not found"
    
    output = {"Endpoints":{f'{old}_extra': [], f'{new}_extra': []}, "Domains":{f'{old}_extra': [], f'{new}_extra': []}, "Differences":[]}
    endpoints = sink.endpoints_coll.find()
    domains = sink.domain_coll.find()

    oldEndpoints = [x for x in endpoints if x['_id']['name'] == old]
    newEndpoints = [x for x in endpoints if x['_id']['name'] == new]

    oldCnames = [x for x in domains if x['_id']['name'] == old]
    newCnames = [x for x in domains if x['_id']['name'] == new]

    for endpoint in oldEndpoints:
        if endpoint not in newEndpoints:
            output['Endpoints'][f'{old}_extra'].append(endpoint['_id']['ip'])
        else:
            newEndpoint = [x for x in newEndpoints if x['_id']['ip'] == endpoint['_id']['ip']][0]
            # output all differences
            for key in endpoint:
                if key != '_id' and endpoint[key] != newEndpoint[key]:
                    output['Differences'][endpoint['_id']['ip']].append({endpoint['_id']['name']:endpoint[key], newEndpoint['_id']['name']:newEndpoint[key]})

    for endpoint in newEndpoints:
        if endpoint not in oldEndpoints:
            output['Endpoints'][f'{new}_extra'].append(endpoint['_id']['ip'])

    for cname in oldCnames:
        if cname not in newCnames:
            output['Domains'][f'{old}_extra'].append(cname['_id']['domain'])

    for cname in newCnames:
        if cname not in oldCnames:
            output['Domains'][f'{new}_extra'].append(cname['_id']['domain'])

    return json.dumps(output)
    