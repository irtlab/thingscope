from pymongo import MongoClient


class DeviceSink:

    def __init__(self, db_url="mongodb://localhost:27017/", db_name='iot'):

        try:
            client = MongoClient()

            self.db_name = db_name

            # Connect with the portnumber and host
            self.client = MongoClient(db_url)

            # Access database
            self.iotdb = self.client[self.db_name]

            # Access collection of the database
            self.endpoints_coll = self.iotdb.endpoints

            self.domain_coll = self.iotdb.domains

            self.devices_coll = self.iotdb.devices

            self.save = True
        except:
            print('Connection to MongoDB failed')


    def print_endpoints(self):
        cursor = self.endpoints_coll.find()
        for record in cursor:
            print(record)


    def is_endpoint_exist(self, ip):
        try:
            if self.save == False:
                return False
            # if endpoint missing, insert
            doc = self.endpoints_coll.find_one({'_id': ip})
            if doc is not None:
                return True

            return False

        except Exception as e:
            print(f'is_endpoint_exist processing exception for {ip} {e}')
            return False

    def is_device_exist(self, device):
        try:
            # if endpoint missing, insert
            doc = self.devices_coll.find_one({'_id': device})
            if doc is not None:
                return True

            return False

        except Exception as e:
            print(f'is_endpoint_exist processing exception for {device} {e}')
            return False

    def save_device(self, device, ip, name):
        device_info = {
            '_id': device,
            'ip': ip,
            'name': name,
            'mac_addr': device,
            'mfgr': 'TBD',
            'device_type': 'TBD',
            'device_tag': 'TBD',
            'enabled': True
        }
        try:
            if self.save:
                result = self.devices_coll.insert_one(device_info)

            print(f'Saved {self.save} {device_info}')
        except Exception as e:
            print(f'save_device exception for {ip} {e}')

    def save_endpoint(self, device_mac, endpoint_info):
        try:
            endpoint_info['device_mac'] = device_mac
            endpoint_info['_id'] = endpoint_info['ip']
            if self.save:
                result = self.endpoints_coll.insert_one(endpoint_info)
            print(f'Saved {self.save} {endpoint_info}')
        except Exception as e:
            print(f'save_endpoints exception for {device_mac} {e}')

    def save_domain_map(self, domain, cnames):
        try:
            if self.save:
                result = self.domain_coll.update_one({'domain': domain}, {'$set': {'cnames': cnames}}, upsert=True)
            print(f'Saved {self.save} {domain} {cnames}')
        except Exception as e:
            print(f'save_domain_map exception for {domain} {e}')


    def fetch_endpoints(self, filter):
        try:
            # if endpoint missing, insert
            docs = self.endpoints_coll.find(filter)
            return docs
        except Exception as e:
            print(f'fetch_endpoints processing exception for  {e}')
            return None
    def update_endpoint_security(self, id, update_blob):
        try:
            if self.save:
                result = self.endpoints_coll.update_one({'_id': id}, {'$set': update_blob}, upsert=True)
            print(f'Saved {self.save} {id} {update_blob}')
        except Exception as e:
            print(f'save_domain_map exception for {id} {e}')

    def update_endpoint_location(self, id, location):
        try:
            if self.save:
                result = self.endpoints_coll.update_one({'_id': id}, {'$set': {'location': location}}, upsert=True)
            print(f'Saved {self.save} {id} {location}')
        except Exception as e:
            print(f'save_domain_map exception for {id} {e}')

    def update_open_ports(self, ip, open_ports):
        try:
            if self.save:
                result = self.devices_coll.update_one({'ip': ip}, {'$set': {'open_ports': open_ports }}, upsert=True)
            print(f'Saved {self.save} {ip} {open_ports}')
        except Exception as e:
            print(f'save_domain_map exception for {ip} {e}')

