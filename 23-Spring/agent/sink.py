from pymongo import MongoClient
import logging


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
            logging.error('Connection to MongoDB failed')

    def is_endpoint_exist(self, ip, name):
        try:
            if self.save == False:
                return False
            # if endpoint missing, insert
            doc = self.endpoints_coll.find_one({'_id': {'ip': ip, 'device': name}})
            if doc is not None:
                return True

            return False

        except Exception as e:
            logging.error(f'is_endpoint_exist processing exception for {ip}/{name},{e}')
            return False

    def is_device_exist(self, name):
        try:
            # if endpoint missing, insert
            doc = self.devices_coll.find_one({'_id': name})
            if doc is not None:
                return True

            return False

        except Exception as e:
            logging.error(f'is_endpoint_exist processing exception for {name} {e}')
            return False

    def save_device(self, device, name, source_location):
        device_info = {
            '_id': name,
            'mac_addr': device,
            'source_location': source_location
        }
        try:
            if self.save:
                result = self.devices_coll.insert_one(device_info)

            logging.info(f'Saved {self.save} {device_info}')
        except Exception as e:
            logging.error(f'save_device exception for {name} {e}')

    def save_endpoint(self, device_mac, name, endpoint_info, source_location):
        try:
            endpoint_info['device_mac'] = device_mac
            endpoint_info['_id'] = {'ip': endpoint_info['ip'], 'name': name}
            endpoint_info['source_location'] = source_location
            if self.save:
                result = self.endpoints_coll.insert_one(endpoint_info)
            logging.info(f'Saved {self.save} {endpoint_info}')
        except Exception as e:
            logging.error(f'save_endpoints exception for {name} {e}')

    def save_domain_map(self, name, domain, cnames, source_location):
        try:
            if self.save:
                result = self.domain_coll.update_one({"_id":{'name': name, 'domain': domain}}, {'$set': {'cnames': cnames}, 'source_location': source_location}, upsert=True)
            logging.info(f'Saved {self.save} {name}/{domain} {cnames}')
        except Exception as e:
            logging.error(f'save_domain_map exception for {name}/{domain} {e}')

    # def fetch_endpoints(self, filter):
    #     try:
    #         # if endpoint missing, insert
    #         docs = self.endpoints_coll.find(filter)
    #         return docs
    #     except Exception as e:
    #         print(f'fetch_endpoints processing exception for  {e}')
    #         return None
    # def update_endpoint_security(self, id, update_blob):
    #     try:
    #         if self.save:
    #             result = self.endpoints_coll.update_one({'_id': id}, {'$set': update_blob}, upsert=True)
    #         print(f'Saved {self.save} {id} {update_blob}')
    #     except Exception as e:
    #         print(f'save_domain_map exception for {id} {e}')

    # def update_endpoint_location(self, id, location):
    #     try:
    #         if self.save:
    #             result = self.endpoints_coll.update_one({'_id': id}, {'$set': {'location': location}}, upsert=True)
    #         print(f'Saved {self.save} {id} {location}')
    #     except Exception as e:
    #         print(f'save_domain_map exception for {id} {e}')

    # def update_open_ports(self, ip, open_ports):
    #     try:
    #         if self.save:
    #             result = self.devices_coll.update_one({'ip': ip}, {'$set': {'open_ports': open_ports }}, upsert=True)
    #         print(f'Saved {self.save} {ip} {open_ports}')
    #     except Exception as e:
    #         print(f'save_domain_map exception for {ip} {e}')

