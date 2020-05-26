import json
import requests
from requests.exceptions import HTTPError

from tqdm import tqdm

from apigee import APIGEE_ADMIN_API_URL
from apigee import auth, console

CREATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps'
DELETE_KEYVALUEMAP_FROM_AN_ENVIRONMENT_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}'
DELETE_KEYVALUEMAP_ENTRY_IN_AN_ENVIRONMENT_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}'
GET_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}'
GET_A_KEYS_VALUE_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}'
LIST_KEYVALUEMAPS_IN_AN_ENVIRONMENT_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps'
UPDATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}'
CREATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries'
UPDATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}'
LIST_KEYS_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/keys?startkey={startkey}&count={count}'


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
        elif format == "dict":
            return maps
        # else:
        #     raise ValueError(format)
        return resp


class Keyvaluemaps:

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

    def create_keyvaluemap_in_an_environment(self, environment, request_body):
        uri = CREATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment)
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_keyvaluemap_from_an_environment(self, environment):
        uri = DELETE_KEYVALUEMAP_FROM_AN_ENVIRONMENT_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment, name=self._map_name)
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_keyvaluemap_entry_in_an_environment(self, environment, entry_name):
        uri = DELETE_KEYVALUEMAP_ENTRY_IN_AN_ENVIRONMENT_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment, name=self._map_name, entry_name=entry_name)
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_keyvaluemap_in_an_environment(self, environment):
        uri = GET_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment, name=self._map_name)
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_a_keys_value_in_an_environment_scoped_keyvaluemap(
        self, environment, entry_name
    ):
        uri = GET_A_KEYS_VALUE_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment, name=self._map_name, entry_name=entry_name)
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_keyvaluemaps_in_an_environment(
        self, environment, prefix=None, format="json"
    ):
        uri = LIST_KEYVALUEMAPS_IN_AN_ENVIRONMENT_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment)
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return KeyvaluemapsSerializer().serialize_details(resp, format, prefix=prefix)

    def update_keyvaluemap_in_an_environment(self, environment, request_body):
        uri = UPDATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment, name=self._map_name)
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def create_an_entry_in_an_environment_scoped_kvm(
        self, environment, entry_name, entry_value
    ):
        uri = CREATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment, name=self._map_name)
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = {"name": entry_name, "value": entry_value}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def update_an_entry_in_an_environment_scoped_kvm(
        self, environment, entry_name, updated_value
    ):
        uri = UPDATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment, name=self._map_name, entry_name=entry_name)
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = {"name": entry_name, "value": updated_value}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def list_keys_in_an_environment_scoped_keyvaluemap(
        self, environment, startkey, count
    ):
        uri = LIST_KEYS_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment, name=self._map_name, startkey=startkey, count=count)
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
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
            self.get_a_keys_value_in_an_environment_scoped_keyvaluemap(environment, entry["name"])
            self.update_an_entry_in_an_environment_scoped_kvm(environment, entry["name"], entry["value"])
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            self.create_an_entry_in_an_environment_scoped_kvm(environment, entry["name"], entry["value"])

    def _delete_entries(self, environment, deleted_keys):
        for idx, entry in enumerate(tqdm(deleted_keys, desc='Deleting', unit='entries')):
            self.delete_keyvaluemap_entry_in_an_environment(environment, entry["name"])

    def push_keyvaluemap(self, environment, file):
        with open(file) as f:
            body = f.read()
        loc_kvm = json.loads(body)
        self._map_name = loc_kvm["name"]
        try:
            env_kvm = self.get_keyvaluemap_in_an_environment(environment).json()
            _, deleted_keys = self._diff_kvms(loc_kvm, env_kvm)
            updated_loc_kvm = {"entry": [entry for entry in loc_kvm["entry"] if entry not in env_kvm["entry"]]}
            if updated_loc_kvm["entry"]:
                for entry in tqdm(updated_loc_kvm["entry"], desc='Updating', unit='entries'):
                        self._create_or_update_entry(environment, entry)
            else:
                console.echo("All entries up-to-date")
            if deleted_keys:
                self._delete_entries(environment, deleted_keys)
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            console.echo(f"Creating {self._map_name}")
            console.echo(self.create_keyvaluemap_in_an_environment(environment, body).text)
