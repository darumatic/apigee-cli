import json

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.references.serializer import ReferencesSerializer

LIST_ALL_REFERENCES_PATH = (
    "{api_url}/v1/organizations/{org_name}/environments/{environment}/references"
)
GET_REFERENCE_PATH = "{api_url}/v1/organizations/{org_name}/environments/{environment}/references/{ref_name}"
DELETE_REFERENCE_PATH = "{api_url}/v1/organizations/{org_name}/environments/{environment}/references/{ref_name}"
CREATE_REFERENCE_PATH = (
    "{api_url}/v1/organizations/{org_name}/environments/{environment}/references"
)
UPDATE_REFERENCE_PATH = "{api_url}/v1/organizations/{org_name}/environments/{environment}/references/{ref_name}"


class References:
    def __init__(self, auth, org_name, ref_name):
        self._auth = auth
        self._org_name = org_name
        self._ref_name = ref_name

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
    def ref_name(self):
        return self._ref_name

    @ref_name.setter
    def ref_name(self, value):
        self._ref_name = value

    def list_all_references(self, environment, prefix=None, format="json"):
        uri = LIST_ALL_REFERENCES_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self._org_name,
            environment=environment,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return ReferencesSerializer().serialize_details(resp, format, prefix=prefix)

    def get_reference(self, environment):
        uri = GET_REFERENCE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self._org_name,
            environment=environment,
            ref_name=self._ref_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_reference(self):
        pass

    def create_reference(self):
        pass

    def update_reference(self):
        pass
