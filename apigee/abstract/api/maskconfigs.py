#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/data-masks"""

import json
from abc import ABC, abstractmethod


class IMaskconfigs:
    def __init__(self, auth, org_name, api_name):
        self._auth = auth
        self._org_name = org_name
        self._api_name = api_name

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

    def __call__(self):
        pass

    @abstractmethod
    def create_data_masks_for_an_api_proxy(self, request_body):
        pass

    @abstractmethod
    def delete_data_masks_for_an_api_proxy(self, maskconfig_name):
        pass

    @abstractmethod
    def get_data_mask_details_for_an_api_proxy(self, maskconfig_name):
        pass

    @abstractmethod
    def list_data_masks_for_an_api_proxy(self):
        pass

    @abstractmethod
    def list_data_masks_for_an_organization(self):
        pass

    @abstractmethod
    def push_data_masks_for_an_api_proxy(self, file):
        pass


class MaskconfigsSerializer:
    def serialize_details(self, maskconfigs, format, prefix=None):
        resp = maskconfigs
        if format == "text":
            return maskconfigs.text
        maskconfigs = maskconfigs.json()
        if prefix:
            maskconfigs = [
                maskconfig
                for maskconfig in maskconfigs
                if maskconfig.startswith(prefix)
            ]
        if format == "json":
            return json.dumps(maskconfigs)
        elif format == "table":
            pass
        # else:
        #     raise ValueError(format)
        return resp
