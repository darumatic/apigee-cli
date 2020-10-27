import json

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.virtualhosts.serializer import VirtualhostsSerializer

CREATE_A_VIRTUAL_HOST_FOR_AN_ENVIRONMENT_PATH = (
    '{api_url}/v1/o/{org_name}/environments/{environment}/virtualhosts'
)
DELETE_A_VIRTUAL_HOST_FROM_AN_ENVIRONMENT_PATH = (
    '{api_url}/v1/o/{org_name}/environments/{environment}/virtualhosts/{virtualhost_name}'
)
GET_A_VIRTUAL_HOST_FOR_AN_ENVIRONMENT_PATH = (
    '{api_url}/v1/o/{org_name}/environments/{environment}/virtualhosts/{virtualhost_name}'
)
LIST_VIRTUAL_HOSTS_FOR_AN_ENVIRONMENT_PATH = (
    '{api_url}/v1/o/{org_name}/environments/{environment}/virtualhosts'
)
UPDATE_VIRTUAL_HOST_FOR_AN_ENVIRONMENT_PATH = (
    '{api_url}/v1/o/{org_name}/environments/{environment}/virtualhosts/{virtualhost_name}'
)


class Virtualhosts:
    def __init__(self, auth, org_name, virtualhost_name):
        self._auth = auth
        self._org_name = org_name
        self._virtualhost_name = virtualhost_name

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
    def virtualhost_name(self):
        return self._virtualhost_name

    @virtualhost_name.setter
    def virtualhost_name(self, value):
        self._virtualhost_name = value

    def create_a_virtual_host_for_an_environment(self):
        pass

    def delete_a_virtual_host_from_an_environment(self):
        pass

    def get_a_virtual_host_for_an_environment(self, environment):
        uri = GET_A_VIRTUAL_HOST_FOR_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self._org_name,
            environment=environment,
            virtualhost_name=self._virtualhost_name,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_virtual_hosts_for_an_environment(self, environment, prefix=None, format='json'):
        uri = LIST_VIRTUAL_HOSTS_FOR_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org_name=self._org_name, environment=environment
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return VirtualhostsSerializer().serialize_details(resp, format, prefix=prefix)

    def update_virtual_host_for_an_environment(self):
        pass
