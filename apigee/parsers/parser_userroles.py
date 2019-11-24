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
        parser = self._parser_userroles.add_parser('add-a-user-to-a-role', help='Add a user to a role.', parents=[self._parent_parser()])
        parser.add_argument('-n', '--name', help='the role name', required=True)
        parser.add_argument('--user-email', help='the email address of the user', required=True)
        parser.set_defaults(func=lambda args: Userroles(args, args.org, args.name).add_a_user_to_a_role(args.user_email))

    def _create_parser(self):
        self._build_add_a_user_to_a_role_argument()
