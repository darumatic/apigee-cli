#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/data-masks"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.maskconfigs import IMaskconfigs
from apigee.util import authorization

class Maskconfigs(IMaskconfigs):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_data_masks_for_an_api_proxy(self, request_body):
        uri = '{0}/v1/organizations/{1}/apis/{2}/maskconfigs' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def delete_data_masks_for_an_api_proxy(self, maskconfig_name):
        uri = '{0}/v1/organizations/{1}/apis/{2}/maskconfigs/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name,
                    maskconfig_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_data_mask_details_for_an_api_proxy(self, maskconfig_name):
        uri = '{0}/v1/organizations/{1}/apis/{2}/maskconfigs/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name,
                    maskconfig_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_data_masks_for_an_api_proxy(self):
        uri = '{0}/v1/organizations/{1}/apis/{2}/maskconfigs' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_data_masks_for_an_organization(self):
        uri = '{0}/v1/organizations/{1}/maskconfigs' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def push_data_masks_for_an_api_proxy(self, file):
        with open(file) as f:
            body = f.read()
        maskconfig = json.loads(body)
        maskconfig_name = maskconfig['name']
        try:
            self.get_data_mask_details_for_an_api_proxy(maskconfig_name)
            print('Updating', maskconfig_name, 'for', self._api_name)
            print(self.create_data_masks_for_an_api_proxy(body).text)
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                print('Creating', maskconfig_name, 'for', self._api_name)
                print(self.create_data_masks_for_an_api_proxy(body).text)
            else:
                raise e
