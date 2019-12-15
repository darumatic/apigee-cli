#!/usr/bin/env python
"""https://apidocs.apigee.com/api-services/content/environment-keyvalue-maps"""

import json
import requests

import progressbar

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.keyvaluemaps import IKeyvaluemaps, KeyvaluemapsSerializer
from apigee.util import authorization

class Keyvaluemaps(IKeyvaluemaps):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_keyvaluemap_in_an_environment(self, environment, request_body):
        uri = '{0}/v1/organizations/{1}/environments/{2}/keyvaluemaps' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def delete_keyvaluemap_from_an_environment(self, environment):
        uri = '{0}/v1/organizations/{1}/environments/{2}/keyvaluemaps/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment,
                    self._map_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def delete_keyvaluemap_entry_in_an_environment(self, environment, entry_name):
        uri = '{0}/v1/organizations/{1}/environments/{2}/keyvaluemaps/{3}/entries/{4}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment,
                    self._map_name,
                    entry_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_keyvaluemap_in_an_environment(self, environment):
        uri = '{0}/v1/organizations/{1}/environments/{2}/keyvaluemaps/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment,
                    self._map_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_a_keys_value_in_an_environment_scoped_keyvaluemap(self, environment, entry_name):
        uri = '{0}/v1/organizations/{1}/environments/{2}/keyvaluemaps/{3}/entries/{4}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment,
                    self._map_name,
                    entry_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_keyvaluemaps_in_an_environment(self, environment, prefix=None):
        uri = '{0}/v1/organizations/{1}/environments/{2}/keyvaluemaps' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return KeyvaluemapsSerializer().serialize_details(resp, 'json', prefix=prefix)

    def update_keyvaluemap_in_an_environment(self, environment, request_body):
        uri = '{0}/v1/organizations/{1}/environments/{2}/keyvaluemaps/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment,
                    self._map_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def create_an_entry_in_an_environment_scoped_kvm(self, environment, entry_name, entry_value):
        uri = '{0}/v1/organizations/{1}/environments/{2}/keyvaluemaps/{3}/entries' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment,
                    self._map_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = {
          'name' : entry_name,
          'value' : entry_value
        }
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def update_an_entry_in_an_environment_scoped_kvm(self, environment, entry_name, updated_value):
        uri = '{0}/v1/organizations/{1}/environments/{2}/keyvaluemaps/{3}/entries/{4}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment,
                    self._map_name,
                    entry_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = {
          'name' : entry_name,
          'value' : updated_value
        }
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_keys_in_an_environment_scoped_keyvaluemap(self, environment, startkey, count):
        uri = '{0}/v1/organizations/{1}/environments/{2}/keyvaluemaps/{3}/keys?startkey={4}&count={5}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment,
                    self._map_name,
                    startkey,
                    count)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        # return KeyvaluemapsSerializer().serialize_details(resp, 'json', prefix=prefix)
        return resp

    def push_keyvaluemap(self, environment, file):
        with open(file) as f:
            body = f.read()
        kvm = json.loads(body)
        self._map_name = kvm['name']
        try:
            keyvaluemap_in_an_environment = self.get_keyvaluemap_in_an_environment(environment).json()

            # get KeyValueMap entries to be deleted
            keys = [_['name'] for _ in kvm['entry']]
            entries_deleted = [_ for _ in keyvaluemap_in_an_environment['entry'] if _['name'] not in keys]

            bar = progressbar.ProgressBar(maxval=len(kvm['entry'])).start()
            print('Updating entries in', self._map_name)

            for idx, entry in enumerate(kvm['entry']):
                if entry not in keyvaluemap_in_an_environment['entry']:
                    try:
                        self.get_a_keys_value_in_an_environment_scoped_keyvaluemap(environment, entry['name'])
                        self.update_an_entry_in_an_environment_scoped_kvm(environment, entry['name'], entry['value'])
                    except requests.exceptions.HTTPError as e:
                        status_code = e.response.status_code
                        if status_code == 404:
                            self.create_an_entry_in_an_environment_scoped_kvm(environment, entry['name'], entry['value'])
                        else:
                            raise e
                bar.update(idx)
            bar.finish()

            if entries_deleted:
                bar = progressbar.ProgressBar(maxval=len(entries_deleted)).start()
                print('Deleting entries in', self._map_name)
                for idx, entry in enumerate(entries_deleted):
                    self.delete_keyvaluemap_entry_in_an_environment(environment, entry['name'])
                    bar.update(idx)
            bar.finish()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                print('Creating', self._map_name)
                print(self.create_keyvaluemap_in_an_environment(environment, body).text)
            else:
                raise e
