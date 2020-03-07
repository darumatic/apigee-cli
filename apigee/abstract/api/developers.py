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
    def create_developer(
        self, first_name, last_name, user_name, attributes='{"attributes" : [ ]}'
    ):
        pass

    @abstractmethod
    def delete_developer(self):
        pass

    @abstractmethod
    def get_developer(self):
        pass

    @abstractmethod
    def get_developer_by_app(self, app_name):
        pass

    @abstractmethod
    def list_developers(self):
        pass

    @abstractmethod
    def set_developer_status(self, action):
        pass

    @abstractmethod
    def update_developer(self, request_body):
        pass

    @abstractmethod
    def get_developer_attribute(self, attribute_name):
        pass

    @abstractmethod
    def update_a_developer_attribute(self, attribute_name, updated_value):
        pass

    @abstractmethod
    def delete_developer_attribute(self, attribute_name):
        pass

    @abstractmethod
    def get_all_developer_attributes(self):
        pass

    @abstractmethod
    def update_all_developer_attributes(self, request_body):
        pass


class DevelopersSerializer:
    def serialize_details(self, developers, format, prefix=None):
        resp = developers
        if format == "text":
            return developers.text
        developers = developers.json()
        if prefix:
            developers = [
                developer for developer in developers if developer.startswith(prefix)
            ]
        if format == "json":
            return json.dumps(developers)
        elif format == "table":
            pass
        # else:
        #     raise ValueError(format)
        return resp
