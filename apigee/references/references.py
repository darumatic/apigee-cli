import json

import requests

from apigee import APIGEE_ADMIN_API_URL, auth
from apigee.references.serializer import ReferencesSerializer

LIST_ALL_REFERENCES_PATH = "{api_url}/v1/organizations/{org_name}/environments/{environment}/references"
GET_REFERENCE_PATH = "{api_url}/v1/organizations/{org_name}/environments/{environment}/references/{ref_name}"
DELETE_REFERENCE_PATH = "{api_url}/v1/organizations/{org_name}/environments/{environment}/references/{ref_name}"
CREATE_REFERENCE_PATH = "{api_url}/v1/organizations/{org_name}/environments/{environment}/references"
UPDATE_REFERENCE_PATH = "{api_url}/v1/organizations/{org_name}/environments/{environment}/references/{ref_name}"


class References:
    def __init__(self, auth, org_name, ref_name):
        self.auth = auth
        self.org_name = org_name
        self.ref_name = ref_name

    def list_all_references(self, environment, prefix=None, format="json"):
        uri = LIST_ALL_REFERENCES_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
        )
        resp = self.fetch_reference_data(uri)
        return ReferencesSerializer().serialize_details(resp, format, prefix=prefix)

    def get_reference(self, environment):
        uri = GET_REFERENCE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
            ref_name=self.ref_name,
        )
        return self.fetch_reference_data(uri)

    def fetch_reference_data(self, uri):
        hdrs = auth.set_authentication_headers(
            self.auth, custom_headers={"Accept": "application/json"}
        )
        result = requests.get(uri, headers=hdrs)
        result.raise_for_status()
        return result
