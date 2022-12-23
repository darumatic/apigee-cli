import json

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.caches.serializer import CachesSerializer
from apigee.utils import read_file

CLEAR_ALL_CACHE_ENTRIES_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/caches/{name}/entries?action=clear"
CLEAR_A_CACHE_ENTRY_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/caches/{name}/entries/{entry}?action=clear"
CREATE_A_CACHE_IN_AN_ENVIRONMENT_PATH = (
    "{api_url}/v1/organizations/{org}/environments/{environment}/caches?name={name}"
)
GET_INFORMATION_ABOUT_A_CACHE_PATH = (
    "{api_url}/v1/organizations/{org}/environments/{environment}/caches/{name}"
)
LIST_CACHES_IN_AN_ENVIRONMENT_PATH = (
    "{api_url}/v1/organizations/{org}/environments/{environment}/caches"
)
UPDATE_A_CACHE_IN_AN_ENVIRONMENT_PATH = (
    "{api_url}/v1/organizations/{org}/environments/{environment}/caches/{name}"
)
DELETE_A_CACHE_PATH = (
    "{api_url}/v1/organizations/{org}/environments/{environment}/caches/{name}"
)


class Caches:
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

    def clear_all_cache_entries(self, environment):
        uri = CLEAR_ALL_CACHE_ENTRIES_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._cache_name,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/octet-stream",
            },
        )
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def clear_a_cache_entry(self, environment, entry):
        uri = CLEAR_A_CACHE_ENTRY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._cache_name,
            entry=entry,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/octet-stream",
            },
        )
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def create_a_cache_in_an_environment(self, environment, request_body):
        uri = CREATE_A_CACHE_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._cache_name,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def get_information_about_a_cache(self, environment):
        uri = GET_INFORMATION_ABOUT_A_CACHE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._cache_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_caches_in_an_environment(self, environment, prefix=None, format="json"):
        uri = LIST_CACHES_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return CachesSerializer().serialize_details(resp, format, prefix=prefix)

    def update_a_cache_in_an_environment(self, environment, request_body):
        uri = UPDATE_A_CACHE_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._cache_name,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_a_cache(self, environment):
        uri = DELETE_A_CACHE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._cache_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def push_cache(self, environment, file):
        cache = read_file(file, type="json")
        self._cache_name = cache["name"]
        try:
            self.get_information_about_a_cache(environment)
            console.echo(f"Updating {self._cache_name}")
            console.echo(
                self.update_a_cache_in_an_environment(
                    environment, json.dumps(cache)
                ).text
            )
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            console.echo(f"Creating {self._cache_name}")
            console.echo(
                self.create_a_cache_in_an_environment(
                    environment, json.dumps(cache)
                ).text
            )
