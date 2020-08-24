import json

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console

CREATE_A_TARGETSERVER_PATH = (
    '{api_url}/v1/organizations/{org}/environments/{environment}/targetservers'
)
DELETE_A_TARGETSERVER_PATH = (
    '{api_url}/v1/organizations/{org}/environments/{environment}/targetservers/{name}'
)
LIST_TARGETSERVERS_IN_AN_ENVIRONMENT_PATH = (
    '{api_url}/v1/organizations/{org}/environments/{environment}/targetservers'
)
GET_TARGETSERVER_PATH = (
    '{api_url}/v1/organizations/{org}/environments/{environment}/targetservers/{name}'
)
UPDATE_A_TARGETSERVER_PATH = (
    '{api_url}/v1/organizations/{org}/environments/{environment}/targetservers/{name}'
)


class TargetserversSerializer:
    def serialize_details(self, targetservers, format, prefix=None):
        resp = targetservers
        if format == 'text':
            return targetservers.text
        targetservers = targetservers.json()
        if prefix:
            targetservers = [
                targetserver
                for targetserver in targetservers
                if targetserver.startswith(prefix)
            ]
        if format == 'json':
            return json.dumps(targetservers)
        elif format == 'table':
            pass
        elif format == 'dict':
            return targetservers
        # else:
        #     raise ValueError(format)
        return resp


class Targetservers:
    def __init__(self, auth, org_name, targetserver_name):
        self._auth = auth
        self._org_name = org_name
        self._targetserver_name = targetserver_name

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
    def targetserver_name(self):
        return self._targetserver_name

    @targetserver_name.setter
    def targetserver_name(self, value):
        self._targetserver_name = value

    def create_a_targetserver(self, environment, request_body):
        uri = CREATE_A_TARGETSERVER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_a_targetserver(self, environment):
        uri = DELETE_A_TARGETSERVER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._targetserver_name,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_targetservers_in_an_environment(self, environment, prefix=None, format='json'):
        uri = LIST_TARGETSERVERS_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return TargetserversSerializer().serialize_details(resp, format, prefix=prefix)

    def get_targetserver(self, environment):
        uri = GET_TARGETSERVER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._targetserver_name,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def update_a_targetserver(self, environment, request_body):
        uri = UPDATE_A_TARGETSERVER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._targetserver_name,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        )
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def push_targetserver(self, environment, file):
        with open(file) as f:
            body = f.read()
        targetserver = json.loads(body)
        self._targetserver_name = targetserver['name']
        try:
            self.get_targetserver(environment)
            console.echo(f'Updating {self._targetserver_name}')
            console.echo(self.update_a_targetserver(environment, body).text)
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            console.echo(f'Creating {self._targetserver_name}')
            console.echo(self.create_a_targetserver(environment, body).text)
