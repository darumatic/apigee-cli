#!/usr/bin/env python
"""https://apidocs.apigee.com/api/apps-developer

https://apidocs.apigee.com/api/developer-app-keys
"""

import json
import random
import requests
import string

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.apps import IApps, AppsSerializer
from apigee.util import authorization

class Apps(IApps):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_developer_app(self, developer, request_body):
        uri = '{0}/v1/organizations/{1}/developers/{2}/apps' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    developer)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def create_empty_developer_app(self, developer, display_name='', callback_url=''):
        uri = '{0}/v1/organizations/{1}/developers/{2}/apps' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    developer)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = {
         "name" : self._app_name,
         # "apiProducts": args.products,
         "attributes" : [
          {
           "name" : "DisplayName",
           "value" : display_name
          }
         ],
         # "scopes" : args.scopes,
         "callbackUrl" : callback_url
        }
        if not display_name:
            del body['attributes']
        if not callback_url:
            del body['callback_url']
        # body = {k: v for k, v in body.items() if v}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        self.delete_key_for_a_developer_app(developer, resp.json()['credentials'][0]['consumerKey'])
        return self.get_developer_app_details(developer)

    def get_developer_app_details(self, developer):
        uri = '{0}/v1/organizations/{1}/developers/{2}/apps/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    developer,
                    self._app_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_developer_apps(self, developer, prefix=None, expand=False, count=100, startkey=''):
        uri = '{0}/v1/organizations/{1}/developers/{2}/apps' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    developer)
        if expand:
            uri += '?expand={0}'.format(expand)
        else:
            uri += '?count={0}&startKey={1}'.format(count, startkey)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return AppsSerializer().serialize_details(resp, 'json', prefix=prefix)

    def delete_key_for_a_developer_app(self, developer, consumer_key):
        uri = '{0}/v1/organizations/{1}/developers/{2}/apps/{3}/keys/{4}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    developer,
                    self._app_name,
                    consumer_key)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def create_a_consumer_key_and_secret(self, developer, consumer_key=None, consumer_secret=None, key_length=32,
                                         secret_length=32, key_suffix=None, key_delimiter='-', products=[]):
        uri = '{0}/v1/organizations/{1}/developers/{2}/apps/{3}/keys/create' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    developer,
                    self._app_name)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        # app = self.get_developer_app_details(developer)
        if not consumer_key:
            consumer_key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(key_length))
        if not consumer_secret:
            consumer_secret = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(secret_length))
        if key_suffix:
            consumer_key += key_delimiter
            consumer_key += key_suffix
        body = {
          "consumerKey": consumer_key,
          "consumerSecret": consumer_secret
        }
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        if products:
            print(resp.text)
            consumer_key = resp.json()['consumerKey']
            request_body = json.dumps({ "apiProducts": products,
              "attributes": resp.json()['attributes']
            })
            print('Adding API Products', products, 'to consumerKey', consumer_key)
            return self.add_api_product_to_key(developer, consumer_key, request_body)
        return resp

    def add_api_product_to_key(self, developer, consumer_key, request_body):
        uri = '{0}/v1/organizations/{1}/developers/{2}/apps/{3}/keys/{4}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    developer,
                    self._app_name,
                    consumer_key)
        hdrs = authorization.set_header({'Accept': 'application/json',
                                         'Content-Type': 'application/json'},
                                        self._auth)
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp
