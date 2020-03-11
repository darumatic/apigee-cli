#!/usr/bin/env python
"""Source: https://apidocs.apigee.com/api/caches

API Platform Base Path: https://api.enterprise.apigee.com/v1/o/{org_name}

API Resource Path: /environments/{env_name}/caches

A lightweight persistence store that can be used by policies or code executing
on the Apigee Edge.

To support data segregation, cache resources are scoped to environments.
"""

import json
import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.caches import ICaches, CachesSerializer
from apigee.util import authorization, console


class Caches(ICaches):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clear_all_cache_entries(self, environment):
        """Clears all entries from the specified cache.

        Entries to be cleared can be scoped by CacheKey prefix by using the
        'prefix' parameter.

        Args:
            environment (str): Apigee environment.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/caches/{self._cache_name}/entries?action=clear"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/octet-stream"},
            self._auth,
        )
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def clear_a_cache_entry(self, environment, entry):
        """Clears a cache entry, which is identified by the full CacheKey prefix
        and value.

        Args:
            environment (str): Apigee environment.
            entry (str): The cache entry to clear.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/caches/{self._cache_name}/entries/{entry}?action=clear"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/octet-stream"},
            self._auth,
        )
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def create_a_cache_in_an_environment(self, environment, request_body):
        """Creates a cache in an environment.

        Args:
            environment (str): Apigee environment.
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/caches?name={self._cache_name}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def get_information_about_a_cache(self, environment):
        """Gets information about a cache.

        The response might contain a property named ``persistent``.
        That property is no longer used by Edge.

        Args:
            environment (str): Apigee environment.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/caches/{self._cache_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_caches_in_an_environment(self, environment, prefix=None):
        """List caches in an environment.

        Args:
            environment (str): Apigee environment.
            prefix (str, optional): Filter results by a prefix string.
                Defaults to None.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/caches"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return CachesSerializer().serialize_details(resp, "json", prefix=prefix)

    def update_a_cache_in_an_environment(self, environment, request_body):
        """Updates a cache in an environment.

        You must specify the complete definition of the cache,
        including the properties that you want to change and the ones that
        retain their current value.
        Any properties omitted from the request body are reset to their default
        value.

        Args:
            environment (str): Apigee environment.
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/caches/{self._cache_name}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_a_cache(self, environment):
        """Deletes a cache.

        Args:
            environment (str): Apigee environment.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/caches/{self._cache_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def push_cache(self, environment, file):
        """Push cache file to Apigee

        This will create a cache if it does not exist and update if it does.

        Args:
            environment (str): Apigee environment.
            file (str): The file path.

        Returns:
            None

        Raises:
            HTTPError: If response status code is not successful or 404.
        """
        with open(file) as f:
            body = f.read()
        cache = json.loads(body)
        self._cache_name = cache["name"]
        try:
            self.get_information_about_a_cache(environment)
            console.log("Updating", self._cache_name)
            console.log(self.update_a_cache_in_an_environment(environment, body).text)
        except HTTPError as e:
            if e.response.status_code not in [404]:
                raise e
            console.log("Creating", self._cache_name)
            console.log(self.create_a_cache_in_an_environment(environment, body).text)
