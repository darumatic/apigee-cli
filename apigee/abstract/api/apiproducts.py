#!/usr/bin/env python
"""https://apidocs.apigee.com/api/api-products-1"""

import json
from abc import ABC, abstractmethod


class IApiproducts:
    def __init__(self, auth, org_name, apiproduct_name):
        self._auth = auth
        self._org_name = org_name
        self._apiproduct_name = apiproduct_name

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
    def apiproduct_name(self):
        return self._apiproduct_name

    @apiproduct_name.setter
    def apiproduct_name(self, value):
        self._apiproduct_name = value

    @abstractmethod
    def create_api_product(self, request_body):
        pass

    @abstractmethod
    def delete_api_product(self):
        pass

    @abstractmethod
    def get_api_product(self):
        pass

    @abstractmethod
    def list_api_products(self, prefix=None, expand=False, count=1000, startkey=""):
        pass

    @abstractmethod
    def update_api_product(self, request_body):
        pass

    @abstractmethod
    def push_apiproducts(self, file):
        pass


class ApiproductsSerializer:
    def serialize_details(self, apiproducts, format, prefix=None):
        resp = apiproducts
        if format == "text":
            return apiproducts.text
        apiproducts = apiproducts.json()
        if prefix:
            apiproducts = [
                apiproduct
                for apiproduct in apiproducts
                if apiproduct.startswith(prefix)
            ]
        if format == "json":
            return json.dumps(apiproducts)
        elif format == "table":
            pass
        # else:
        #     raise ValueError(format)
        return resp
