#!/usr/bin/env python
"""https://apidocs.apigee.com/api/api-products-1"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.apiproducts import IApiproducts, ApiproductsSerializer
from apigee.util import authorization

class Apiproducts(IApiproducts):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_api_product(self, request_body):
        uri = '{0}/v1/organizations/{1}/apiproducts' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def delete_api_product(self):
        uri = '{0}/v1/organizations/{1}/apiproducts/{2}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._apiproduct_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def get_api_product(self):
        uri = '{0}/v1/organizations/{1}/apiproducts/{2}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._apiproduct_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_api_products(self, prefix=None, expand=False, count=1000, startkey=''):
        uri = '{0}/v1/organizations/{1}/apiproducts?expand={2}&count={3}&startKey={4}' \
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
        return ApiproductsSerializer().serialize_details(resp, 'json', prefix=prefix)

    def update_api_product(self, request_body):
        uri = '{0}/v1/organizations/{1}/apiproducts/{2}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._apiproduct_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def push_apiproducts(self, file):
        with open(file) as f:
            body = f.read()
        apiproduct = json.loads(body)
        self._apiproduct_name = apiproduct['name']
        try:
            self.get_api_product()
            print('Updating', self._apiproduct_name)
            print(self.update_api_product(body).text)
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                print('Creating', self._apiproduct_name)
                print(self.create_api_product(body).text)
            else:
                raise e
