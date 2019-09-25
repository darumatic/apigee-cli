#!/usr/bin/env python
"""https://apidocs.apigee.com/api-services/content/environment-keyvalue-maps"""

import json
from abc import ABC, abstractmethod


class IKeyvaluemaps:
    def __init__(self, auth, org_name, map_name):
        self._auth = auth
        self._org_name = org_name
        self._map_name = map_name

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
    def map_name(self):
        return self._map_name

    @map_name.setter
    def map_name(self, value):
        self._map_name = value

    @abstractmethod
    def create_keyvaluemap_in_an_environment(self, environment, request_body):
        pass

    @abstractmethod
    def delete_keyvaluemap_from_an_environment(self, environment):
        pass

    @abstractmethod
    def delete_keyvaluemap_entry_in_an_environment(self, environment, entry_name):
        pass

    @abstractmethod
    def get_keyvaluemap_in_an_environment(self, environment):
        pass

    @abstractmethod
    def get_a_keys_value_in_an_environment_scoped_keyvaluemap(
        self, environment, entry_name
    ):
        pass

    @abstractmethod
    def list_keyvaluemaps_in_an_environment(self, environment, prefix=None):
        pass

    @abstractmethod
    def update_keyvaluemap_in_an_environment(self, environment, request_body):
        pass

    @abstractmethod
    def create_an_entry_in_an_environment_scoped_kvm(
        self, environment, entry_name, entry_value
    ):
        pass

    @abstractmethod
    def update_an_entry_in_an_environment_scoped_kvm(
        self, environment, entry_name, updated_value
    ):
        pass

    @abstractmethod
    def list_keys_in_an_environment_scoped_keyvaluemap(
        self, environment, startkey, count
    ):
        pass

    @abstractmethod
    def push_keyvaluemap(self, environment, file):
        pass


class KeyvaluemapsSerializer:
    def serialize_details(self, maps, format, prefix=None):
        resp = maps
        if format == "text":
            return maps.text
        maps = maps.json()
        if prefix:
            maps = [map for map in maps if map.startswith(prefix)]
        if format == "json":
            return json.dumps(maps)
        elif format == "table":
            pass
        # else:
        #     raise ValueError(format)
        return resp
