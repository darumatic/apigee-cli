import json

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.maskconfigs.serializer import MaskconfigsSerializer
from apigee.utils import read_file

CREATE_DATA_MASKS_FOR_AN_API_PROXY_PATH = (
    "{api_url}/v1/organizations/{org}/apis/{api_name}/maskconfigs"
)
DELETE_DATA_MASKS_FOR_AN_API_PROXY_PATH = (
    "{api_url}/v1/organizations/{org}/apis/{api_name}/maskconfigs/{maskconfig_name}"
)
GET_DATA_MASK_DETAILS_FOR_AN_API_PROXY_PATH = (
    "{api_url}/v1/organizations/{org}/apis/{api_name}/maskconfigs/{maskconfig_name}"
)
LIST_DATA_MASKS_FOR_AN_API_PROXY_PATH = (
    "{api_url}/v1/organizations/{org}/apis/{api_name}/maskconfigs"
)
LIST_DATA_MASKS_FOR_AN_ORGANIZATION_PATH = (
    "{api_url}/v1/organizations/{org}/maskconfigs"
)


class Maskconfigs:
    def __init__(self, auth, org_name, api_name):
        self._auth = auth
        self._org_name = org_name
        self._api_name = api_name

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

    def __call__(self):
        pass

    def create_data_masks_for_an_api_proxy(self, request_body):
        uri = CREATE_DATA_MASKS_FOR_AN_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, api_name=self._api_name
        )
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_data_masks_for_an_api_proxy(self, maskconfig_name):
        uri = DELETE_DATA_MASKS_FOR_AN_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            api_name=self._api_name,
            maskconfig_name=maskconfig_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_data_mask_details_for_an_api_proxy(self, maskconfig_name):
        uri = GET_DATA_MASK_DETAILS_FOR_AN_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            api_name=self._api_name,
            maskconfig_name=maskconfig_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_data_masks_for_an_api_proxy(self):
        uri = LIST_DATA_MASKS_FOR_AN_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, api_name=self._api_name
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_data_masks_for_an_organization(self):
        uri = LIST_DATA_MASKS_FOR_AN_ORGANIZATION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def push_data_masks_for_an_api_proxy(self, file):
        maskconfig = read_file(file, type="json")
        maskconfig_name = maskconfig["name"]
        try:
            self.get_data_mask_details_for_an_api_proxy(maskconfig_name)
            console.echo(f"Updating {maskconfig_name} for {self._api_name}")
            console.echo(
                self.create_data_masks_for_an_api_proxy(json.dumps(maskconfig)).text
            )
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            console.echo(f"Creating {maskconfig_name} for {self._api_name}")
            console.echo(
                self.create_data_masks_for_an_api_proxy(json.dumps(maskconfig)).text
            )
