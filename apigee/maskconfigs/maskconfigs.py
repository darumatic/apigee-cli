import json

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.utils import read_file_content

CREATE_DATA_MASKS_FOR_AN_API_PROXY_PATH = "{api_url}/v1/organizations/{org}/apis/{api_name}/maskconfigs"
DELETE_DATA_MASKS_FOR_AN_API_PROXY_PATH = "{api_url}/v1/organizations/{org}/apis/{api_name}/maskconfigs/{maskconfig_name}"
GET_DATA_MASK_DETAILS_FOR_AN_API_PROXY_PATH = "{api_url}/v1/organizations/{org}/apis/{api_name}/maskconfigs/{maskconfig_name}"
LIST_DATA_MASKS_FOR_AN_API_PROXY_PATH = "{api_url}/v1/organizations/{org}/apis/{api_name}/maskconfigs"
LIST_DATA_MASKS_FOR_AN_ORGANIZATION_PATH = "{api_url}/v1/organizations/{org}/maskconfigs"


class Maskconfigs:
    def __init__(self, auth, org_name, api_name):
        self.auth = auth
        self.org_name = org_name
        self.api_name = api_name

    def create_data_masks_for_an_api_proxy(self, request_body):
        uri = CREATE_DATA_MASKS_FOR_AN_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, api_name=self.api_name
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_data_masks_for_an_api_proxy(self, maskconfig_name):
        uri = DELETE_DATA_MASKS_FOR_AN_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            api_name=self.api_name,
            maskconfig_name=maskconfig_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_data_mask_details_for_an_api_proxy(self, maskconfig_name):
        uri = GET_DATA_MASK_DETAILS_FOR_AN_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            api_name=self.api_name,
            maskconfig_name=maskconfig_name,
        )
        return self.fetch_data_masks_for_organization(uri)

    def list_data_masks_for_an_api_proxy(self):
        uri = LIST_DATA_MASKS_FOR_AN_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, api_name=self.api_name
        )
        return self.fetch_data_masks_for_organization(uri)

    def list_data_masks_for_an_organization(self):
        uri = LIST_DATA_MASKS_FOR_AN_ORGANIZATION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name
        )
        return self.fetch_data_masks_for_organization(uri)

    def fetch_data_masks_for_organization(self, uri):
        hdrs = auth.set_authentication_headers(
            self.auth, custom_headers={"Accept": "application/json"}
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def push_data_masks_for_an_api_proxy(self, file):
        maskconfig = read_file_content(file, type="json")
        maskconfig_name = maskconfig["name"]
        try:
            self.get_data_mask_details_for_an_api_proxy(maskconfig_name)
            console.echo(f"Updating {maskconfig_name} for {self.api_name}")
            console.echo(
                self.create_data_masks_for_an_api_proxy(json.dumps(maskconfig)).text
            )
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            console.echo(f"Creating {maskconfig_name} for {self.api_name}")
            console.echo(
                self.create_data_masks_for_an_api_proxy(json.dumps(maskconfig)).text
            )
