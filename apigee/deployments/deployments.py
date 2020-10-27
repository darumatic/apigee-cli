import json

import requests
from tabulate import tabulate

from apigee import APIGEE_ADMIN_API_URL, auth
from apigee.deployments.serializer import DeploymentsSerializer

GET_API_PROXY_DEPLOYMENT_DETAILS_PATH = (
    '{api_url}/v1/organizations/{org}/apis/{api_name}/deployments'
)


class Deployments:
    def __init__(self, auth, org_name, api_name):
        self._auth = auth
        self._org_name = org_name
        self._api_name = api_name

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
    def api_name(self):
        return self._api_name

    @api_name.setter
    def api_name(self, value):
        self._api_name = value

    def get_api_proxy_deployment_details(
        self,
        formatted=False,
        format='text',
        showindex=False,
        tablefmt='plain',
        revision_name_only=False,
    ):
        uri = GET_API_PROXY_DEPLOYMENT_DETAILS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, api_name=self._api_name
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        if formatted:
            if revision_name_only:
                return DeploymentsSerializer().serialize_details(
                    resp, format, showindex=showindex, tablefmt=tablefmt
                )
            return DeploymentsSerializer().serialize_details(resp, 'text')
        return resp
