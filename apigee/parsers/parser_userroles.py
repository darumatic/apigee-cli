import argparse

from apigee.api.userroles import Userroles

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.prefix_parser import PrefixParser

class ParserUserroles:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_userroles = self._parser.add_parser('userroles', aliases=['roles'], help='manage user roles').add_subparsers()
        self._parent_parser = kwargs.get('parent_parser', ParentParser())
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def parser_userroles(self):
        return self._parser_userroles

    @parser_userroles.setter
    def parser_userroles(self, value):
        self._parser_userroles = value

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    def __call__(self):
        return self._parser

    def _build_add_a_user_to_a_role_argument(self):
        parser = self._parser_userroles.add_parser('add-user', aliases=['add-a-user-to-a-role'], help='Add a user to a role.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.add_argument('--user-email', help='the email address of the user', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).add_a_user_to_a_role(args.user_email).text))

    def _build_add_permissions_for_a_resource_to_a_user_role_argument(self):
        parser = self._parser_userroles.add_parser('add-permissions', aliases=['add-permissions-for-a-resource-to-a-user-role'], help='Add Permissions for Resource to a Role', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.add_argument('-b', '--body', help='request body', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).add_permissions_for_a_resource_to_a_user_role(args.body).text))

    def _build_add_permissions_for_multiple_resources_to_a_user_role_argument(self):
        parser = self._parser_userroles.add_parser('add-permissions-multiple', aliases=['add-permissions-for-multiple-resources-to-a-user-role'], help='Adds multiple permissions to multiple resources simultaneously.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='name', required=True)
        parser.add_argument('-b', '--body', help='request body', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).add_permissions_for_multiple_resources_to_a_user_role(args.body).text))

    def _build_create_a_user_role_in_an_organization_argument(self):
        parser = self._parser_userroles.add_parser('create', aliases=['create-a-user-role-in-an-organization'], help='Creates one ore more user roles in an organization.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', nargs='+', help='list of role names', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).create_a_user_role_in_an_organization().text))

    def _build_delete_a_permission_for_a_resource_argument(self):
        parser = self._parser_userroles.add_parser('delete-permission', aliases=['delete-a-permission-for-a-resource'], help='Removes a permission from a resource for the role specified. Permissions are case sensitive. Specify the permission as get, put, or delete.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.add_argument('--permission', help='get, put, or delete', required=True)
        parser.add_argument('--resource-path', help='the resource path', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).delete_a_permission_for_a_resource(args.permission, args.resource_path).text))

    def _build_delete_resource_from_permissions_argument(self):
        parser = self._parser_userroles.add_parser('delete-resource', aliases=['delete-resource-from-permissions'], help='Removes all permissions for a resource for the role specified. Permissions are case sensitive.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.add_argument('--resource-path', help='the resource path', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).delete_resource_from_permissions(args.resource_path).text))

    def _build_delete_a_user_role_argument(self):
        parser = self._parser_userroles.add_parser('delete', aliases=['delete-a-user-role'], help='Deletes a role from an organization. Roles can only be deleted when no users are in the role.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).delete_a_user_role().text))

    def _build_get_a_role_argument(self):
        parser = self._parser_userroles.add_parser('get', aliases=['get-a-role'], help='Gets the name of a user role.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).get_a_role().text))

    def _build_get_resource_permissions_for_a_specific_role_argument(self):
        parser = self._parser_userroles.add_parser('get-permissions', aliases=['get-resource-permissions-for-a-specific-role'], help='Gets a list of permissions associated with the specified resource.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.add_argument('--resource-path', help='the resource path', default='')
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).get_resource_permissions_for_a_specific_role(resource_path=args.resource_path).text))

    def _build_get_users_for_a_role_argument(self):
        parser = self._parser_userroles.add_parser('get-users', aliases=['get-users-for-a-role'], help='Returns a list of all system users associated with a role.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).get_users_for_a_role().text))

    def _build_list_permissions_for_a_resource_argument(self):
        parser = self._parser_userroles.add_parser('list-permissions', aliases=['list-permissions-for-a-resource'], help='Gets permissions for all resources associated with a user role.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).list_permissions_for_a_resource().text))

    def _build_list_user_roles_argument(self):
        parser = self._parser_userroles.add_parser('list', aliases=['list-user-roles'], help='Gets a list of roles available to users in an organization.', parents=[self._parent_parser()])
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, None).list_user_roles().text))

    def _build_remove_user_membership_in_role_argument(self):
        parser = self._parser_userroles.add_parser('remove-user', aliases=['remove-user-membership-in-role'], help='Remove user membership in role.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.add_argument('--user-email', help='the email address of the user', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).remove_user_membership_in_role(args.user_email).text))

    def _build_verify_a_user_roles_permission_on_a_specific_RBAC_resource_argument(self):
        parser = self._parser_userroles.add_parser('verify-permission', aliases=['verify-a-user-roles-permission-on-a-specific-RBAC-resource'], help="Verifies that a user role's permission on a specific resource exists. Returns a value of true or false.", parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.add_argument('--permission', help='get, put, or delete', required=True)
        parser.add_argument('--resource-path', help='the resource path', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).verify_a_user_roles_permission_on_a_specific_RBAC_resource(args.permission, args.resource_path).text))

    def _build_verify_user_role_membership_argument(self):
        parser = self._parser_userroles.add_parser('verify-membership', aliases=['verify-user-role-membership'], help='Verify user role membership.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.add_argument('--user-email', help='the email address of the user', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).verify_user_role_membership(args.user_email).text))

    def _create_parser(self):
        self._build_add_a_user_to_a_role_argument()
        self._build_add_permissions_for_a_resource_to_a_user_role_argument()
        self._build_add_permissions_for_multiple_resources_to_a_user_role_argument()
        self._build_create_a_user_role_in_an_organization_argument()
        self._build_delete_a_permission_for_a_resource_argument()
        self._build_delete_resource_from_permissions_argument()
        self._build_delete_a_user_role_argument()
        self._build_get_a_role_argument()
        self._build_get_resource_permissions_for_a_specific_role_argument()
        self._build_get_users_for_a_role_argument()
        self._build_list_permissions_for_a_resource_argument()
        self._build_list_user_roles_argument()
        self._build_remove_user_membership_in_role_argument()
        self._build_verify_a_user_roles_permission_on_a_specific_RBAC_resource_argument()
        self._build_verify_user_role_membership_argument()
