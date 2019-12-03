#!/usr/bin/env python
"""https://apidocs.apigee.com/api/apps-developer

https://apidocs.apigee.com/api/developer-app-keys
"""

import json
from abc import ABC, abstractmethod

class IApps:

    def __init__(self, auth, org_name, app_name):
        self._auth = auth
        self._org_name = org_name
        self._app_name = app_name

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
    def app_name(self):
        return self._app_name

    @app_name.setter
    def app_name(self, value):
        self._app_name = value

    def __call__(self):
        pass

    @abstractmethod
    def create_developer_app(self, developer, request_body):
        pass

    @abstractmethod
    def create_empty_developer_app(self, developer, display_name='', callback_url=''):
        pass

    @abstractmethod
    def get_developer_app_details(self, developer):
        pass

    @abstractmethod
    def list_developer_apps(self, developer, prefix=None, expand=False, count=100, startkey=''):
        pass

    @abstractmethod
    def delete_key_for_a_developer_app(self, developer, consumer_key):
        pass

    @abstractmethod
    def create_a_consumer_key_and_secret(self, developer, consumer_key=None, consumer_secret=None, key_length=32, secret_length=32, key_suffix=None, key_delimiter='-', products=[]):
        pass

    @abstractmethod
    def add_api_product_to_key(self, developer, consumer_key, request_body):
        pass

class AppsSerializer:
    def serialize_details(self, apps, format, prefix=None):
        resp = apps
        if format == 'text':
            return apps.text
        apps = apps.json()
        if prefix:
            apps = [app for app in apps if app.startswith(prefix)]
        if format == 'json':
            return json.dumps(apps)
        elif format == 'table':
            pass
        # else:
        #     raise ValueError(format)
        return resp
