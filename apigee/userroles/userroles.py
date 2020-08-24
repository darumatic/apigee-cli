import json

import requests

from apigee import APIGEE_ADMIN_API_URL, auth

ADD_A_USER_TO_A_ROLE_PATH = (
    '{api_url}/v1/organizations/{org}/userroles/{role_name}/users?id={user_email}'
)
ADD_PERMISSIONS_FOR_A_RESOURCE_TO_A_USER_ROLE_PATH = (
    '{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions'
)
ADD_PERMISSIONS_FOR_MULTIPLE_RESOURCES_TO_A_USER_ROLE_PATH = (
    '{api_url}/v1/organizations/{org}/userroles/{role_name}/resourcepermissions'
)
CREATE_A_USER_ROLE_IN_AN_ORGANIZATION_PATH = '{api_url}/v1/organizations/{org}/userroles'
DELETE_A_PERMISSION_FOR_A_RESOURCE_PATH = '{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions/{permission}?path={resource_path}'
DELETE_RESOURCE_FROM_PERMISSIONS_PATH = '{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions?path={resource_path}&delete=true'
DELETE_A_USER_ROLE_PATH = '{api_url}/v1/organizations/{org}/userroles/{role_name}'
GET_A_ROLE_PATH = '{api_url}/v1/organizations/{org}/userroles/{role_name}'
GET_RESOURCE_PERMISSIONS_FOR_A_SPECIFIC_ROLE_PATH = (
    '{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions'
)
GET_USERS_FOR_A_ROLE_PATH = '{api_url}/v1/organizations/{org}/userroles/{role_name}/users'
LIST_PERMISSIONS_FOR_A_RESOURCE_PATH = (
    '{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions'
)
LIST_USER_ROLES_PATH = '{api_url}/v1/organizations/{org}/userroles'
REMOVE_USER_MEMBERSHIP_IN_ROLE_PATH = (
    '{api_url}/v1/organizations/{org}/userroles/{role_name}/users/{user_email}'
)
VERIFY_A_USER_ROLES_PERMISSION_ON_A_SPECIFIC_RBAC_RESOURCE_PATH = '{api_url}/v1/organizations/{org}/userroles/{role_name}/permissions/{permission}?path={resource_path}'
VERIFY_USER_ROLE_MEMBERSHIP_PATH = (
    '{api_url}/v1/organizations/{org}/userroles/{role_name}/users/{user_email}'
)


class Userroles:
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

    def add_a_user_to_a_role(self, user_email):
        uri = ADD_A_USER_TO_A_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            role_name=self._role_name,
            user_email=user_email,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        )
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def add_permissions_for_a_resource_to_a_user_role(self, request_body):
        uri = ADD_PERMISSIONS_FOR_A_RESOURCE_TO_A_USER_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, role_name=self._role_name
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def add_permissions_for_multiple_resources_to_a_user_role(self, request_body):
        uri = f'{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/userroles/{self._role_name}/resourcepermissions'
        uri = ADD_PERMISSIONS_FOR_MULTIPLE_RESOURCES_TO_A_USER_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, role_name=self._role_name
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def create_a_user_role_in_an_organization(self):
        uri = CREATE_A_USER_ROLE_IN_AN_ORGANIZATION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        )
        roles = []
        for role in self._role_name:
            roles.append({'name': role})
        body = {'role': roles}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_a_permission_for_a_resource(self, permission, resource_path):
        uri = DELETE_A_PERMISSION_FOR_A_RESOURCE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            role_name=self._role_name,
            permission=permission,
            resource_path=resource_path,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/octet-stream'},
        )
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_resource_from_permissions(self, resource_path):
        uri = DELETE_RESOURCE_FROM_PERMISSIONS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            role_name=self._role_name,
            resource_path=resource_path,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/octet-stream'},
        )
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_a_user_role(self):
        uri = DELETE_A_USER_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, role_name=self._role_name
        )
        hdrs = auth.set_header(
            self._auth,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        )
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_a_role(self):
        uri = GET_A_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, role_name=self._role_name
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_resource_permissions_for_a_specific_role(self, resource_path=""):
        uri = GET_RESOURCE_PERMISSIONS_FOR_A_SPECIFIC_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, role_name=self._role_name
        )
        if resource_path:
            uri += f'?path={resource_path}'
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/octet-stream'},
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_users_for_a_role(self):
        uri = GET_USERS_FOR_A_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, role_name=self._role_name
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_permissions_for_a_resource(self):
        uri = LIST_PERMISSIONS_FOR_A_RESOURCE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, role_name=self._role_name
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_user_roles(self):
        uri = LIST_USER_ROLES_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name)
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def remove_user_membership_in_role(self, user_email):
        uri = REMOVE_USER_MEMBERSHIP_IN_ROLE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            role_name=self._role_name,
            user_email=user_email,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        )
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def verify_a_user_roles_permission_on_a_specific_RBAC_resource(
        self, permission, resource_path
    ):
        uri = VERIFY_A_USER_ROLES_PERMISSION_ON_A_SPECIFIC_RBAC_RESOURCE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            role_name=self._role_name,
            permission=permission,
            resource_path=resource_path,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/octet-stream'},
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def verify_user_role_membership(self, user_email):
        uri = VERIFY_USER_ROLE_MEMBERSHIP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            role_name=self._role_name,
            user_email=user_email,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp
