#!/usr/bin/env python
"""Source: https://apidocs.apigee.com/api-reference/content/data-masks

Base Path: https://api.enterprise.apigee.com/v1/o/{org_name}

API Resource Path: /maskconfigs

Specify data that will be filtered out of trace sessions

Edge enables developers to capture message content to enable runtime debugging
of APIs calls.
In many cases, API traffic contains sensitive data, such credit cards or
personally identifiable health information (PHI)
that needs to filtered out of the captured message content.
Mask configurations enable you to specify data that will be filtered out of
trace sessions.
Masking configurations can be set globally (at the organization-level) or
locally (at the API proxy level).
"""

import json
import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.maskconfigs import IMaskconfigs
from apigee.util import authorization, console


class Maskconfigs(IMaskconfigs):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_data_masks_for_an_api_proxy(self, request_body):
        """Create a data mask for an API proxy.

        Args:
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/apis/{self._api_name}/maskconfigs"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_data_masks_for_an_api_proxy(self, maskconfig_name):
        """Delete a data mask for an API proxy.

        Args:
            maskconfig_name (str): The data mask to delete.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/apis/{self._api_name}/maskconfigs/{maskconfig_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_data_mask_details_for_an_api_proxy(self, maskconfig_name):
        """Get the details for a data mask for an API proxy.

        Args:
            maskconfig_name (str): The data mask name.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/apis/{self._api_name}/maskconfigs/{maskconfig_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_data_masks_for_an_api_proxy(self):
        """List all data masks for an API proxy.

        Args:
            None

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/apis/{self._api_name}/maskconfigs"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_data_masks_for_an_organization(self):
        """List all data masks for an organization.

        Args:
            None

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/maskconfigs"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def push_data_masks_for_an_api_proxy(self, file):
        """Push data mask file to Apigee

        This will create a data mask if it does not exist and update if it does.

        Args:
            environment (str): Apigee environment.
            file (str): The file path.

        Returns:
            None

        Raises:
            HTTPError: If response status code is not successful or 404.
        """
        with open(file) as f:
            body = f.read()
        maskconfig = json.loads(body)
        maskconfig_name = maskconfig["name"]
        try:
            self.get_data_mask_details_for_an_api_proxy(maskconfig_name)
            console.log("Updating", maskconfig_name, "for", self._api_name)
            console.log(self.create_data_masks_for_an_api_proxy(body).text)
        except HTTPError as e:
            if e.response.status_code not in [404]:
                raise e
            console.log("Creating", maskconfig_name, "for", self._api_name)
            console.log(self.create_data_masks_for_an_api_proxy(body).text)
