#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import json
from abc import ABC, abstractmethod

class IApis:

    def __init__(self, auth, org_name, api_name):
        self._auth = auth
        self._org_name = org_name
        self._api_name = api_name

    def __call__(self):
        pass

    @property
    def auth(self):
        return self._auth

    @auth.setter
    def auth(self, value):
        self._auth = value

    @property
    def org_name(self):
        return self._org_name

    @org_name.setter
    def org_name(self, value):
        self._org_name = value

    @property
    def api_name(self):
        return self._api_name

    @api_name.setter
    def api_name(self, value):
        self._api_name = value

    def delete_api_proxy_revision(self, revision_number):
        pass

    def delete_undeployed_revisions(self, save_last=0, dry_run=False):
        pass

    def export_api_proxy(self, revision_number, writezip=True, output_file=None):
        pass

    def get_api_proxy(self):
        pass

    def list_api_proxies(self, prefix=None):
        pass

    def list_api_proxy_revisions(self):
        pass

class ApisSerializer:
    def serialize_details(self, apis, format, prefix=None):
        resp = apis
        if format == 'text':
            return apis.text
        apis = apis.json()
        if prefix:
            apis = [api for api in apis if api.startswith(prefix)]
        if format == 'json':
            return json.dumps(apis)
        elif format == 'table':
            pass
        # else:
        #     raise ValueError(format)
        return resp
