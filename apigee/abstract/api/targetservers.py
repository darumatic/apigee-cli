#!/usr/bin/env python
"""https://apidocs.apigee.com/api/api_resources/51-targetservers"""

import json
from abc import ABC, abstractmethod

class ITargetservers:

    def __init__(self, auth, org_name, targetserver_name):
        self._auth = auth
        self._org_name = org_name
        self._targetserver_name = targetserver_name

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
    def targetserver_name(self):
        return self._targetserver_name

    @targetserver_name.setter
    def targetserver_name(self, value):
        self._targetserver_name = value

    @abstractmethod
    def create_a_targetserver(self, environment, request_body):
        pass

    @abstractmethod
    def delete_a_targetserver(self, environment):
        pass

    @abstractmethod
    def list_targetservers_in_an_environment(self, environment, prefix=None):
        pass

    @abstractmethod
    def get_targetserver(self, environment):
        pass

    @abstractmethod
    def update_a_targetserver(self, environment, request_body):
        pass

    @abstractmethod
    def push_targetserver(self, environment, file):
        pass

class TargetserversSerializer:
    def serialize_details(self, targetservers, format, prefix=None):
        resp = targetservers
        if format == 'text':
            return targetservers.text
        targetservers = targetservers.json()
        if prefix:
            targetservers = [targetserver for targetserver in targetservers if targetserver.startswith(prefix)]
        if format == 'json':
            return json.dumps(targetservers)
        elif format == 'table':
            pass
        # else:
        #     raise ValueError(format)
        return resp
