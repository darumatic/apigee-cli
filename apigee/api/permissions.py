#!/usr/bin/env python
"""Source: https://docs.apigee.com/api-platform/system-administration/permissions

Manage permissions that you can assign to a role by using the Edge API.
"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.permissions import IPermissions, PermissionsSerializer
from apigee.util import authorization


class Permissions(IPermissions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_permissions(self, request_body):
        """Creates permissions for a role.

        Args:
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/resourcepermissions"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def team_permissions(
        self, template_file, placeholder_key=None, placeholder_value=""
    ):
        """Creates permissions for a role using a template file.

        Args:
            template_file (str): The template file path.
            placeholder_key (str, optional): The placeholder key to replace with
                a placeholder value.
                Defaults to None.
            placeholder_value (str, optional): The placeholder value to replace
                placeholder key.
                Default to ''.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/resourcepermissions"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        with open(template_file) as f:
            body = json.loads(f.read())
        if placeholder_key:
            for idx, resource_permission in enumerate(body["resourcePermission"]):
                path = resource_permission["path"]
                body["resourcePermission"][idx]["path"] = path.replace(
                    placeholder_key, placeholder_value
                )
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def get_permissions(
        self, formatted=False, format="text", showindex=False, tablefmt="plain"
    ):
        """Gets permissions for a role.

        Args:
            formatted (bool, optional): If True, format ``requests.Response()``.
                Defaults to False.
            format (str, optional): Specify how to format response.
                Defaults to 'text'.
            showindex (bool, optional): If True, show table index.
                Defaults to False.
            tablefmt (str, optional): Specify table format. Defaults to 'plain'.

        Returns:
            requests.Response(): Response if ``formatted`` is False, else return
            a ``formatted`` value.
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/o/{self._org_name}/userroles/{self._role_name}/permissions"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        if formatted:
            return PermissionsSerializer().serialize_details(
                resp, format, showindex=showindex, tablefmt=tablefmt
            )
        return resp
