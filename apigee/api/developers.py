#!/usr/bin/env python
"""https://apidocs.apigee.com/api/developers-0"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.developers import IDevelopers, DevelopersSerializer
from apigee.util import authorization

class Developers(IDevelopers):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_developer(self, first_name, last_name, user_name, attributes='{"attributes" : [ ]}'):
        uri = '{0}/v1/organizations/{1}/developers' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = {
           "email" : self._developer_email,
           "firstName" : first_name,
           "lastName" : last_name,
           "userName" : user_name,
           "attributes" : json.loads(attributes)['attributes']
        }
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def delete_developer(self):
        uri = '{0}/v1/organizations/{1}/developers/{2}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._developer_email)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_developer(self):
        uri = '{0}/v1/organizations/{1}/developers/{2}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._developer_email)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_developer_by_app(self, app_name):
        uri = '{0}/v1/organizations/{1}/developers?app={2}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    app_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_developers(self, prefix=None, expand=False, count=100, startkey=''):
        uri = '{0}/v1/organizations/{1}/developers?expand={2}&count={3}&startKey={4}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    expand,
                    count,
                    startkey)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return DevelopersSerializer().serialize_details(resp, 'json', prefix=prefix)

    def set_developer_status(self, action):
        uri = '{0}/v1/organizations/{1}/developers/{2}?action={3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._developer_email,
                    action)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/octet-stream'},
                                        self._auth)
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def update_developer(self, request_body):
        uri = '{0}/v1/organizations/{1}/developers/{2}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._developer_email)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_developer_attribute(self, attribute_name):
        uri = '{0}/v1/organizations/{1}/developers/{2}/attributes/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._developer_email,
                    attribute_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def update_a_developer_attribute(self, attribute_name, updated_value):
        uri = '{0}/v1/organizations/{1}/developers/{2}/attributes/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._developer_email,
                    attribute_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        body = {"value" : updated_value}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def delete_developer_attribute(self, attribute_name):
        uri = '{0}/v1/organizations/{1}/developers/{2}/attributes/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._developer_email,
                    attribute_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_all_developer_attributes(self):
        uri = '{0}/v1/organizations/{1}/developers/{2}/attributes' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._developer_email)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def update_all_developer_attributes(self, request_body):
        uri = '{0}/v1/organizations/{1}/developers/{2}/attributes' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._developer_email)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp
