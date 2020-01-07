#!/usr/bin/env python
"""https://apidocs.apigee.com/api/caches"""

import json
from abc import ABC, abstractmethod

class ICaches:

    def __init__(self, auth, org_name, cache_name):
        self._auth = auth
        self._org_name = org_name
        self._cache_name = cache_name

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
    def cache_name(self):
        return self._cache_name

    @cache_name.setter
    def cache_name(self, value):
        self._cache_name = value

    @abstractmethod
    def clear_all_cache_entries(self, environment):
        pass

    @abstractmethod
    def clear_a_cache_entry(self, environment, entry):
        pass

    @abstractmethod
    def create_a_cache_in_an_environment(self, environment, request_body):
        pass

    @abstractmethod
    def get_information_about_a_cache(self, environment):
        pass

    @abstractmethod
    def list_caches_in_an_environment(self, environment, prefix=None):
        pass

    @abstractmethod
    def update_a_cache_in_an_environment(self, environment, request_body):
        pass

    @abstractmethod
    def delete_a_cache(self, environment):
        pass

    @abstractmethod
    def push_cache(self, environment, file):
        pass

class CachesSerializer:
    def serialize_details(self, caches, format, prefix=None):
        resp = caches
        if format == 'text':
            return caches.text
        caches = caches.json()
        if prefix:
            caches = [cache for cache in caches if cache.startswith(prefix)]
        if format == 'json':
            return json.dumps(caches)
        elif format == 'table':
            pass
        # else:
        #     raise ValueError(format)
        return resp
