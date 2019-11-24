import argparse

from apigee.api.userroles import Userroles

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.prefix_parser import PrefixParser

class ParserUserroles:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_userroles = self._parser.add_parser('userroles', help='manage user roles').add_subparsers()
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

    def _build_delete_a_user_role_argument(self):
        parser = self._parser_userroles.add_parser('delete', aliases=['delete-a-user-role'], help='Deletes a role from an organization. Roles can only be deleted when no users are in the role.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).delete_a_user_role().text))

    def _build_remove_user_membership_in_role_argument(self):
        parser = self._parser_userroles.add_parser('remove-user', aliases=['remove-user-membership-in-role'], help='Remove user membership in role.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.add_argument('--user-email', help='the email address of the user', required=True)
        parser.set_defaults(func=lambda args: print(Userroles(args, args.org, args.name).remove_user_membership_in_role(args.user_email).text))

    def _create_parser(self):
        self._build_add_a_user_to_a_role_argument()
        self._build_create_a_user_role_in_an_organization_argument()
        self._build_delete_a_permission_for_a_resource_argument()
        self._build_delete_a_user_role_argument()
        self._build_remove_user_membership_in_role_argument()
