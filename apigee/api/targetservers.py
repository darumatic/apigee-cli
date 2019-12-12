#!/usr/bin/env python
"""https://apidocs.apigee.com/api/api_resources/51-targetservers"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.targetservers import ITargetservers, TargetserversSerializer
from apigee.util import authorization

class Targetservers(ITargetservers):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_a_targetserver(self, environment, request_body):
        uri = '{0}/v1/organizations/{1}/environments/{2}/targetservers' \
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

    def delete_a_targetserver(self, environment):
        uri = '{0}/v1/organizations/{1}/environments/{2}/targetservers/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment,
                    self._targetserver_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_targetservers_in_an_environment(self, environment, prefix=None):
        uri = '{0}/v1/organizations/{1}/environments/{2}/targetservers' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return TargetserversSerializer().serialize_details(resp, 'json', prefix=prefix)

    def get_targetserver(self, environment):
        uri = '{0}/v1/organizations/{1}/environments/{2}/targetservers/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment,
                    self._targetserver_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def update_a_targetserver(self, environment, request_body):
        uri = '{0}/v1/organizations/{1}/environments/{2}/targetservers/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    environment,
                    self._targetserver_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def push_targetserver(self, environment, file):
        with open(file) as f:
            body = f.read()
        targetserver = json.loads(body)
        self._targetserver_name = targetserver['name']
        try:
            self.get_targetserver(environment)
            print('Updating', self._targetserver_name)
            print(self.update_a_targetserver(environment, body).text)
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                print('Creating', self._targetserver_name)
                print(self.create_a_targetserver(environment, body).text)
            else:
                raise e
