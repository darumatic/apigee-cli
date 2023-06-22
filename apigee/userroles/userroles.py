import json

import requests

from apigee import APIGEE_ADMIN_API_URL, auth

ADD_A_USER_TO_A_ROLE_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/users?id={user_email}"
ADD_PERMISSIONS_FOR_A_RESOURCE_TO_A_USER_ROLE_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions"
ADD_PERMISSIONS_FOR_MULTIPLE_RESOURCES_TO_A_USER_ROLE_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/resourcepermissions"
CREATE_A_USER_ROLE_IN_AN_ORGANIZATION_PATH = "{api_url}/v1/organizations/{org}/userroles"
DELETE_A_PERMISSION_FOR_A_RESOURCE_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions/{permission}?path={resource_path}"
DELETE_RESOURCE_FROM_PERMISSIONS_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions?path={resource_path}&delete=true"
DELETE_A_USER_ROLE_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}"
GET_A_ROLE_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}"
GET_RESOURCE_PERMISSIONS_FOR_A_SPECIFIC_ROLE_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions"
GET_USERS_FOR_A_ROLE_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/users"
LIST_PERMISSIONS_FOR_A_RESOURCE_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions"
LIST_USER_ROLES_PATH = "{api_url}/v1/organizations/{org}/userroles"
REMOVE_USER_MEMBERSHIP_IN_ROLE_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/users/{user_email}"
VERIFY_A_USER_ROLES_PERMISSION_ON_A_SPECIFIC_RBAC_RESOURCE_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions/{permission}?path={resource_path}"
VERIFY_USER_ROLE_MEMBERSHIP_PATH = "{api_url}/v1/organizations/{org}/userroles/{role_name}/users/{user_email}"


class Userroles:
    def __init__(self, auth, org_name, role_name):
        self.auth = auth
        self.org_name = org_name
        self.role_name = role_name

    def add_a_user_to_a_role(self, user_email):
        uri = ADD_A_USER_TO_A_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            role_name=self.role_name,
            user_email=user_email,
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def add_permissions_for_a_resource_to_a_user_role(self, request_body):
        return self.add_permissions_for_multiple_resources_to_user_role(
            ADD_PERMISSIONS_FOR_A_RESOURCE_TO_A_USER_ROLE_PATH, request_body
        )

    def add_permissions_for_multiple_resources_to_a_user_role(self, request_body):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self.org_name}/userroles/{self.role_name}/resourcepermissions"
        return self.add_permissions_for_multiple_resources_to_user_role(
            ADD_PERMISSIONS_FOR_MULTIPLE_RESOURCES_TO_A_USER_ROLE_PATH,
            request_body,
        )

    def add_permissions_for_multiple_resources_to_user_role(self, endpoint_template, request_body):
        uri = endpoint_template.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            role_name=self.role_name,
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        body = json.loads(request_body)
        return self.create_user_role_in_organization(
            uri, hdrs, body
        )

    def create_a_user_role_in_an_organization(self, roles):
        uri = CREATE_A_USER_ROLE_IN_AN_ORGANIZATION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = {"role": [{"name": role} for role in roles]}
        return self.create_user_role_in_organization(
            uri, hdrs, body
        )

    def create_user_role_in_organization(self, uri, headers, request_body):
        resp = requests.post(uri, headers=headers, json=request_body)
        resp.raise_for_status()
        return resp

    def delete_a_permission_for_a_resource(self, permission, resource_path):
        uri = DELETE_A_PERMISSION_FOR_A_RESOURCE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            role_name=self.role_name,
            permission=permission,
            resource_path=resource_path,
        )
        return self.remove_user_membership_from_role(
            "application/octet-stream", uri
        )

    def delete_a_user_role(self):
        uri = DELETE_A_USER_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, role_name=self.role_name
        )
        return self.remove_user_membership_from_role(
            "application/x-www-form-urlencoded", uri
        )

    def delete_resource_from_permissions(self, resource_path):
        uri = DELETE_RESOURCE_FROM_PERMISSIONS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            role_name=self.role_name,
            resource_path=resource_path,
        )
        return self.remove_user_membership_from_role(
            "application/octet-stream", uri
        )

    def get_a_role(self):
        uri = GET_A_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, role_name=self.role_name
        )
        return self.verify_and_fetch_user_role_membership(
            "application/json", uri
        )

    def get_resource_permissions_for_a_specific_role(self, resource_path=""):
        uri = GET_RESOURCE_PERMISSIONS_FOR_A_SPECIFIC_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, role_name=self.role_name
        )
        if resource_path:
            uri += f"?path={resource_path}"
        return self.verify_and_fetch_user_role_membership(
            "application/octet-stream", uri
        )

    def get_users_for_a_role(self):
        uri = GET_USERS_FOR_A_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, role_name=self.role_name
        )
        return self.verify_and_fetch_user_role_membership(
            "application/json", uri
        )

    def list_permissions_for_a_resource(self):
        uri = LIST_PERMISSIONS_FOR_A_RESOURCE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, role_name=self.role_name
        )
        return self.verify_and_fetch_user_role_membership(
            "application/json", uri
        )

    def list_user_roles(self):
        uri = LIST_USER_ROLES_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name
        )
        return self.verify_and_fetch_user_role_membership(
            "application/json", uri
        )

    def remove_user_membership_from_role(self, content_type, uri):
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": content_type},
        )
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def remove_user_membership_in_role(self, user_email):
        uri = REMOVE_USER_MEMBERSHIP_IN_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            role_name=self.role_name,
            user_email=user_email,
        )
        return self.remove_user_membership_from_role(
            "application/json", uri
        )

    @staticmethod
    def sort_resource_permissions(resource_permissions):
        permissions_list = resource_permissions.get("resourcePermission")

        for permission_entry in range(len(permissions_list)):
            permission_entry["permissions"].sort()

        return resource_permissions

    def verify_a_user_roles_permission_on_a_specific_RBAC_resource(
        self, permission, resource_path
    ):
        uri = VERIFY_A_USER_ROLES_PERMISSION_ON_A_SPECIFIC_RBAC_RESOURCE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            role_name=self.role_name,
            permission=permission,
            resource_path=resource_path,
        )
        return self.verify_and_fetch_user_role_membership(
            "application/octet-stream", uri
        )

    def verify_and_fetch_user_role_membership(self, content_type, uri):
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": content_type},
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def verify_user_role_membership(self, user_email):
        uri = VERIFY_USER_ROLE_MEMBERSHIP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            role_name=self.role_name,
            user_email=user_email,
        )
        return self.verify_and_fetch_user_role_membership(
            "application/json", uri
        )
