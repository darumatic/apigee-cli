import json

import requests

from apigee import APIGEE_ADMIN_API_URL, auth
from apigee.permissions.serializer import PermissionsSerializer

CREATE_PERMISSIONS_PATH = (
    "{api_url}/v1/organizations/{org}/userroles/{role_name}/resourcepermissions"
)
TEAM_PERMISSIONS_PATH = (
    "{api_url}/v1/organizations/{org}/userroles/{role_name}/resourcepermissions"
)
GET_PERMISSIONS_PATH = "{api_url}/v1/o/{org}/userroles/{role_name}/permissions"


class Permissions:
    def __init__(self, auth, org_name, role_name):
        self._auth = auth
        self._org_name = org_name
        self._role_name = role_name

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
    def role_name(self):
        return self._role_name

    @role_name.setter
    def role_name(self, value):
        self._role_name = value

    def create_permissions(self, request_body):
        uri = CREATE_PERMISSIONS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, role_name=self._role_name
        )
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def team_permissions(
        self, template_file, placeholder_key=None, placeholder_value=""
    ):
        uri = TEAM_PERMISSIONS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, role_name=self._role_name
        )
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
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
        uri = GET_PERMISSIONS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, role_name=self._role_name
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        if formatted:
            return PermissionsSerializer().serialize_details(
                resp, format, showindex=showindex, tablefmt=tablefmt
            )
        return resp
