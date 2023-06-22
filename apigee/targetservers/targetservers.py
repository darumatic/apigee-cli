import json

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.targetservers.serializer import TargetserversSerializer
from apigee.utils import read_file_content

CREATE_A_TARGETSERVER_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/targetservers"
DELETE_A_TARGETSERVER_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/targetservers/{name}"
LIST_TARGETSERVERS_IN_AN_ENVIRONMENT_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/targetservers"
GET_TARGETSERVER_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/targetservers/{name}"
UPDATE_A_TARGETSERVER_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/targetservers/{name}"


class Targetservers:
    def __init__(self, auth, org_name, targetserver_name):
        self.auth = auth
        self.org_name = org_name
        self.targetserver_name = targetserver_name

    def create_a_targetserver(self, environment, request_body):
        uri = CREATE_A_TARGETSERVER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, environment=environment
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_a_targetserver(self, environment):
        uri = DELETE_A_TARGETSERVER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            name=self.targetserver_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_targetservers_in_an_environment(
        self, environment, prefix=None, format="json"
    ):
        uri = LIST_TARGETSERVERS_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, environment=environment
        )
        resp = self.fetch_target_server_data(uri)
        return TargetserversSerializer().serialize_details(resp, format, prefix=prefix)

    def get_targetserver(self, environment):
        uri = GET_TARGETSERVER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            name=self.targetserver_name,
        )
        return self.fetch_target_server_data(uri)

    def fetch_target_server_data(self, uri):
        hdrs = auth.set_authentication_headers(
            self.auth, custom_headers={"Accept": "application/json"}
        )
        result = requests.get(uri, headers=hdrs)
        result.raise_for_status()
        return result

    def update_a_targetserver(self, environment, request_body):
        uri = UPDATE_A_TARGETSERVER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            name=self.targetserver_name,
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def push_targetserver(self, environment, file):
        targetserver = read_file_content(file, type="json")
        self.targetserver_name = targetserver["name"]
        try:
            self.get_targetserver(environment)
            console.echo(f"Updating {self.targetserver_name}")
            console.echo(
                self.update_a_targetserver(environment, json.dumps(targetserver)).text
            )
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            console.echo(f"Creating {self.targetserver_name}")
            console.echo(
                self.create_a_targetserver(environment, json.dumps(targetserver)).text
            )
