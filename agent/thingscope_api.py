import sys
import json
import requests
import traceback


class JWTData:
    def __init__(self, jwt_data):
        if jwt_data is None:
            raise Exception('Authorization failed')
        if not jwt_data['access_token'] or not jwt_data['refresh_token']:
            raise Exception('Authorization failed')
        self.access_token = jwt_data['access_token']
        self.refresh_token = jwt_data['refresh_token']


class ThingScopeAPI:
    def __init__(self):
        self.api_key = '5f7fa6c24816a06e310ca8af'
        self.secret_key = '406dd70950a5f82c1a45777e91baeca6149581cf0f29084a7d5da6225e60908e'
        self.url = 'https://thingscope.cs.columbia.edu/api'

        payload = {'api_key': self.api_key, 'secret_key': self.secret_key}
        try:
            res = self.api_request('POST', self.url + '/agent/sign_in', payload)
            self.jwt_data = JWTData(res)
        except Exception as e:
            traceback.print_exc()
            sys.exit(0)

    def sign_out(self):
        auth = {'access_token': self.jwt_data.access_token, 'refresh_token': self.jwt_data.refresh_token}
        headers = {'authorization': json.dumps(auth)}
        self.api_request('GET', self.url + '/agent/sign_out', {}, headers)


    def get_headers(self):
        return {'authorization': self.jwt_data.access_token}


    def make_request(self, req_type, url, payload, headers = {}):
        try:
            res = None
            if req_type == 'POST':
                res = requests.post(url, json=payload, headers=headers)
            elif req_type == 'GET':
                res = requests.get(url, json=payload, headers=headers)
            return res
        except Exception as e:
            traceback.print_exc()
        return None


    def api_request(self, req_type, url, payload, headers = {}):
        res = self.make_request(req_type, url, payload, headers)
        if res is None:
            return None
        if res.status_code == 401:
            # Update access token and repeat the request.
            tmp_url = self.url + '/agent/' + self.api_key + '/update_access_token'
            rv = self.make_request('POST', tmp_url, {'refresh_token': self.jwt_data.refresh_token})
            if rv and rv.status_code == 200 and rv.text:
                self.jwt_data = JWTData(rv.json())
            else:
                raise Exception('Failed to update access token')
            updated_headers = self.get_headers()
            res = self.make_request(req_type, url, payload, updated_headers)
        if res.status_code == 200 and res.text:
            try:
                data = res.json()
                return data
            except Exception as e:
                return None
        return res


    def insert(self, dev_schema):
        """
        Method stores the given device schema and returns stored schema which
        also contains a unique _id property.

        Args:
        -dev_schema: Device schema to be stored.
        """
        headers = self.get_headers()
        rv = self.api_request('POST', self.url + '/device', dev_schema, headers)
        if rv is None:
            raise Exception('Failed to store device schema')
        return rv


    def update(self, dev_id, update):
        """
        Method updates a device schema by the given ID and returns updated schema.

        Args:
        -dev_id: Unique ID of the device schema. _id property.
        -dev_schema: Device schema to be stored.
        """
        headers = self.get_headers()
        url = self.url + '/device/' + str(dev_id)
        rv = self.api_request('POST', url, update, headers)
        if rv is None:
            raise Exception('Failed to update device schema')
        return rv


    def get_devices(self):
        """Returns a list of devices"""
        return self.api_request('GET', self.url + '/device', {})


    def get_device(self, dev_id):
        """Returns a device by the given device ID"""
        return self.api_request('GET', self.url + '/device/' + str(dev_id), {})
