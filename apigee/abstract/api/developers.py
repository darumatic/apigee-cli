#!/usr/bin/env python
"""https://apidocs.apigee.com/api/developers-0"""

import json
from abc import ABC, abstractmethod

class IDevelopers:

    def __init__(self, auth, org_name, developer_email):
        self._auth = auth
        self._org_name = org_name
        self._developer_email = developer_email

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
    def developer_email(self):
        return self._developer_email

    @developer_email.setter
    def developer_email(self, value):
        self._developer_email = value

    def __call__(self):
        pass

    @abstractmethod
    def list_developers(self):
        pass

class DevelopersSerializer:
    def serialize_details(self, developers, format, prefix=None):
        resp = developers
        if format == 'text':
            return developers.text
        developers = developers.json()
        if prefix:
            developers = [developer for developer in developers if developer.startswith(prefix)]
        if format == 'json':
            return json.dumps(developers)
        elif format == 'table':
            pass
        # else:
        #     raise ValueError(format)
        return resp
