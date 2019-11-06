import argparse

from apigee.api import permissions

from apigee.parsers.parent_parser import ParentParser

class ParserPermissions:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_permissions = self._parser.add_parser('perms', aliases=['permissions'], help='manage permissions for a role').add_subparsers()
        self._parent_parser = kwargs.get('parent_parser', ParentParser())
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def parser_permissions(self):
        return self._parser_permissions

    @parser_permissions.setter
    def parser_permissions(self, value):
        self._parser_permissions = value

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    def __call__(self):
        return self._parser

    def _build_create_permissions_argument(self):
        create_permissions = self._parser_permissions.add_parser('create', aliases=['create-permissions'], parents=[self._parent_parser()],
            help='Create permissions for a role.')
        create_permissions.add_argument('-n', '--name', help='name', required=True)
        create_permissions.add_argument('-b', '--body', help='request body', required=True)
        create_permissions.set_defaults(func=lambda args: print(permissions.create_permissions(args).text))

    def _build_team_permissions_argument(self):
        team_permissions = self._parser_permissions.add_parser('team', aliases=['team-permissions'], parents=[self._parent_parser()],
            help='Create default permissions for a team role based on a template.')
        team_permissions.add_argument('-n', '--name', help='name of user role', required=True)
        team_permissions.add_argument('-t', '--team', help='team prefix/code', required=True)
        team_permissions.set_defaults(func=lambda args: print(permissions.team_permissions(args).text))

    def _build_get_permissions_argument(self):
        get_permissions = self._parser_permissions.add_parser('get', aliases=['get-permissions'], parents=[self._parent_parser()],
            help='Get permissions for a role.')
        get_permissions.add_argument('-n', '--name', help='name', required=True)
        get_permissions.add_argument('-j', '--json', action='store_true', help='use json output')
        get_permissions.add_argument('--max-colwidth', help='max column width', type=int, default=40)
        get_permissions.set_defaults(func=lambda args: print(permissions.get_permissions(args)))

    def _create_parser(self):
        self._build_create_permissions_argument()
        self._build_team_permissions_argument()
        self._build_get_permissions_argument()
