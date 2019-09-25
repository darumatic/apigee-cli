#!/usr/bin/env python
"""Source: https://apidocs.apigee.com/api-services/content/environment-keyvalue-maps

The Key/Value maps API lets you create and manage collections of arbitrary
key/value pairs at the environment scope (for example, test or prod) for
longer-term data persistence.
"""

import json
import requests
from requests.exceptions import HTTPError

from tqdm import tqdm

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.keyvaluemaps import IKeyvaluemaps, KeyvaluemapsSerializer
from apigee.util import authorization, console


class Keyvaluemaps(IKeyvaluemaps):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_keyvaluemap_in_an_environment(self, environment, request_body):
        """Creates a key value map in an environment.

        A key value map is a simple structure for persistently storing
        name/value pairs as entries in a named map.
        The entries in a KVM can be retrieved at runtime by the Key Value Map
        Operations policy or code running on Apigee Edge.
        Use KVMs for use cases such as profile-based access control, storing
        environment-specific data, to control application-specific behavior,
        and so on.

        You can created an encrypted KVM by adding "encrypted" : "true" to the
        payload.

        KVM names are case sensitive.

        Args:
            environment (str): Apigee environment.
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/keyvaluemaps"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_keyvaluemap_from_an_environment(self, environment):
        """Deletes a key/value map and all associated entries from an
        environment.

        Args:
            environment (str): Apigee environment.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/keyvaluemaps/{self._map_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_keyvaluemap_entry_in_an_environment(self, environment, entry_name):
        """Deletes a specific key/value map entry in an environment by name,
        along with associated entries.

        Args:
            environment (str): Apigee environment.
            entry_name (str): The entry to delete.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/keyvaluemaps/{self._map_name}/entries/{entry_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_keyvaluemap_in_an_environment(self, environment):
        """Gets a KeyValueMap (KVM) in an environment by name, along with the
        keys and values.

        KVM names are case sensitive.

        With Apigee Edge for Public Cloud, this API returns only the first 100
        keys in a KVM.

        Args:
            environment (str): Apigee environment.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/keyvaluemaps/{self._map_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_a_keys_value_in_an_environment_scoped_keyvaluemap(
        self, environment, entry_name
    ):
        """Gets the value of a key in an environment-scoped KeyValueMap (KVM).

        Args:
            environment (str): Apigee environment.
            entry_name (str): The entry name.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/keyvaluemaps/{self._map_name}/entries/{entry_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_keyvaluemaps_in_an_environment(self, environment, prefix=None):
        """Lists the name of all key/value maps in an environment.

        Optionally returns an expanded view of all key/value maps for the
        environment.

        Args:
            environment (str): Apigee environment.
            prefix (str, optional): Filter results by a prefix string.
                Defaults to None.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/keyvaluemaps"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return KeyvaluemapsSerializer().serialize_details(resp, "json", prefix=prefix)

    def update_keyvaluemap_in_an_environment(self, environment, request_body):
        """Updates an existing KeyValueMap in an environment.

        Note: This API is supported for Apigee Edge for Private Cloud only.
        For Apigee Edge for Public Cloud use Update an entry in an
        environment-scoped KVM.

        Does not override the existing map. Instead, this method updates the
        entries if they exist or adds them if not.

        It can take several minutes before the new value is visible to runtime
        traffic.

        Args:
            environment (str): Apigee environment.
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/keyvaluemaps/{self._map_name}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def create_an_entry_in_an_environment_scoped_kvm(
        self, environment, entry_name, entry_value
    ):
        """Creates an entry in an existing KeyValueMap scoped to an environment.

        Note: This API is supported for Apigee Edge for the Public Cloud only.

        A key (name) cannot be larger than 2 KB. KVM names are case sensitive.

        Args:
            environment (str): Apigee environment.
            entry_name (str): The entry name to create.
            entry_value (str): The entry value to create.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/keyvaluemaps/{self._map_name}/entries"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = {"name": entry_name, "value": entry_value}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def update_an_entry_in_an_environment_scoped_kvm(
        self, environment, entry_name, updated_value
    ):
        """Updates an entry in a KeyValueMap scoped to an environment.

        Note: This API is supported for Apigee Edge for the Public Cloud only.

        A key cannot be larger than 2 KB. KVM names are case sensitive.

        Does not override the existing map.
        Instead, this method updates the entries if they exist or adds them if
        not.
        It can take several minutes before the new value is visible to runtime
        traffic.

        Args:
            environment (str): Apigee environment.
            entry_name (str): The entry name to update.
            updated_value (str): The new entry value.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/keyvaluemaps/{self._map_name}/entries/{entry_name}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = {"name": entry_name, "value": updated_value}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def list_keys_in_an_environment_scoped_keyvaluemap(
        self, environment, startkey, count
    ):
        """Lists keys in a KeyValueMap scoped to an environment.

        Note: This API is supported for Apigee Edge for the Public Cloud only.

        Args:
            environment (str): Apigee environment.
            startkey (str): To filter the keys that are returned, enter the name
                of a key that the list will start with.
            count (int): Limits the list of keys to the number you specify, up
                to a maximum of 100.
                Use with the startkey parameter to provide more targeted
                filtering.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/keyvaluemaps/{self._map_name}/keys?startkey={startkey}&count={count}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # return KeyvaluemapsSerializer().serialize_details(resp, 'json', prefix=prefix)
        return resp

    def _diff_kvms(self, kvm1, kvm2):
        current_keys = [entry["name"] for entry in kvm1["entry"]]
        deleted_keys = [
            entry for entry in kvm2["entry"] if entry["name"] not in current_keys
        ]
        return current_keys, deleted_keys

    def _create_or_update_entry(self, environment, entry):
        try:
            self.get_a_keys_value_in_an_environment_scoped_keyvaluemap(
                environment, entry["name"]
            )
            self.update_an_entry_in_an_environment_scoped_kvm(
                environment, entry["name"], entry["value"]
            )
        except HTTPError as e:
            if e.response.status_code not in [404]:
                raise e
            self.create_an_entry_in_an_environment_scoped_kvm(
                environment, entry["name"], entry["value"]
            )

    def _delete_entries(self, environment, deleted_keys):
        for idx, entry in enumerate(tqdm(deleted_keys)):
            self.delete_keyvaluemap_entry_in_an_environment(environment, entry["name"])

    def push_keyvaluemap(self, environment, file):
        """Push KeyValueMap file to Apigee

        This will create a KeyValueMap if it does not exist and update if it
        does.

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
        loc_kvm = json.loads(body)
        self._map_name = loc_kvm["name"]
        try:
            env_kvm = self.get_keyvaluemap_in_an_environment(environment).json()
            _, deleted_keys = self._diff_kvms(loc_kvm, env_kvm)
            console.log("Updating entries in", self._map_name)
            for idx, entry in enumerate(tqdm(loc_kvm["entry"])):
                if entry not in env_kvm["entry"]:
                    self._create_or_update_entry(environment, entry)
            if deleted_keys:
                console.log("Deleting entries in", self._map_name)
                self._delete_entries(environment, deleted_keys)
        except HTTPError as e:
            if e.response.status_code not in [404]:
                raise e
            console.log("Creating", self._map_name)
            console.log(
                self.create_keyvaluemap_in_an_environment(environment, body).text
            )
