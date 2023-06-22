import json

import requests

from apigee import APIGEE_ADMIN_API_URL, auth
from apigee.permissions.serializer import PermissionsSerializer

CREATE_PERMISSIONS_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/resourcepermissions"
TEAM_PERMISSIONS_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/resourcepermissions"
GET_PERMISSIONS_PATH = "{api_url}/v1/o/{org}/userroles/{role_name}/permissions"


class Permissions:
    def __init__(self, auth, org_name, role_name):
        self.auth = auth
        self.org_name = org_name
        self.role_name = role_name

    def create_role_permissions(self, request_body):
        uri = CREATE_PERMISSIONS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, role_name=self.role_name
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        return self.send_create_role_permissions_request(uri, hdrs, body)

    def apply_team_permissions_template(
        self, template_file, placeholder_key=None, placeholder_value=""
    ):
        uri = TEAM_PERMISSIONS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, role_name=self.role_name
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        with open(template_file) as f:
            body = json.loads(f.read())
        if placeholder_key:
            for index, resource_permission in enumerate(body["resourcePermission"]):
                path = resource_permission["path"]
                body["resourcePermission"][index]["path"] = path.replace(
                    placeholder_key, placeholder_value
                )
        return self.send_create_role_permissions_request(uri, hdrs, body)

    def send_create_role_permissions_request(self, uri, hdrs, body):
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def get_permissions(
        self, formatted=False, format="text", showindex=False, tablefmt="plain"
    ):
        uri = GET_PERMISSIONS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, role_name=self.role_name
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        if formatted:
            return PermissionsSerializer().serialize_details(
                resp, format, showindex=showindex, tablefmt=tablefmt
            )
        return resp
