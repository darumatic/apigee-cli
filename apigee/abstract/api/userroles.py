#!/usr/bin/env python
"""https://apidocs.apigee.com/api/user-roles"""

from abc import ABC, abstractmethod

class IUserroles:

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

    @abstractmethod
    def add_a_user_to_a_role(self, user_email):
        pass

    @abstractmethod
    def add_permissions_for_a_resource_to_a_user_role(self, request_body):
        pass

    @abstractmethod
    def add_permissions_for_multiple_resources_to_a_user_role(self, request_body):
        pass

    @abstractmethod
    def create_a_user_role_in_an_organization(self):
        pass

    @abstractmethod
    def delete_a_permission_for_a_resource(self, permission, resource_path):
        pass

    @abstractmethod
    def delete_resource_from_permissions(self, resource_path):
        pass

    @abstractmethod
    def delete_a_user_role(self):
        pass

    @abstractmethod
    def get_a_role(self):
        pass

    @abstractmethod
    def get_resource_permissions_for_a_specific_role(self, resource_path=''):
        pass

    @abstractmethod
    def get_users_for_a_role(self):
        pass

    @abstractmethod
    def list_permissions_for_a_resource(self):
        pass

    @abstractmethod
    def list_user_roles(self):
        pass

    @abstractmethod
    def remove_user_membership_in_role(self, user_email):
        pass

    @abstractmethod
    def verify_a_user_roles_permission_on_a_specific_RBAC_resource(self, permission, resource_path):
        pass

    @abstractmethod
    def verify_user_role_membership(self, user_email):
        pass
