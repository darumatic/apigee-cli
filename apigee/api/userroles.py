#!/usr/bin/env python
"""Source: https://apidocs.apigee.com/api/user-roles

API Platform Base Path: https://api.enterprise.apigee.com/v1/o/{org_name}

API Resource Path: /userroles

Roles for users in an organization on Apigee Edge.

User roles form the basis of role-based access in Apigee Edge.

Users are associated with one or more userroles. Each userrole defines a set of
permissions (GET, PUT, DELETE) on RBAC resources (defined by URI paths).

A userrole is scoped to an organization.
"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.userroles import IUserroles
from apigee.util import authorization


class Userroles(IUserroles):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_a_user_to_a_role(self, user_email):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/users?id={user_email}"
        hdrs = authorization.set_header(
            {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            self._auth,
        )
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def add_permissions_for_a_resource_to_a_user_role(self, request_body):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/permissions"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def add_permissions_for_multiple_resources_to_a_user_role(self, request_body):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/resourcepermissions"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def create_a_user_role_in_an_organization(self):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        roles = []
        for role in self._role_name:
            roles.append({"name": role})
        body = {"role": roles}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_a_permission_for_a_resource(self, permission, resource_path):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/permissions/{permission}?path={resource_path}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/octet-stream"},
            self._auth,
        )
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_resource_from_permissions(self, resource_path):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/permissions?path={resource_path}&delete=true"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/octet-stream"},
            self._auth,
        )
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_a_user_role(self):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}"
        hdrs = authorization.set_header(
            {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            self._auth,
        )
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_a_role(self):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_resource_permissions_for_a_specific_role(self, resource_path=""):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/permissions"
        if resource_path:
            uri += f"?path={resource_path}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/octet-stream"},
            self._auth,
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_users_for_a_role(self):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/users"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_permissions_for_a_resource(self):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/permissions"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_user_roles(self):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def remove_user_membership_in_role(self, user_email):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/users/{user_email}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def verify_a_user_roles_permission_on_a_specific_RBAC_resource(
        self, permission, resource_path
    ):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/permissions/{permission}?path={resource_path}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/octet-stream"},
            self._auth,
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def verify_user_role_membership(self, user_email):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/users/{user_email}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp
