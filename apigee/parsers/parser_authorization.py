import argparse
import json

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.file_parser import FileParser
from apigee.util import authorization, mfa_with_pyotp

class ParserAuthorization:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_auth = self._parser.add_parser('authorization', aliases=['auth'], help='verify authorization').add_subparsers()
        self._parent_parser = kwargs.get('parent_parser', ParentParser())
        self._file_parser = kwargs.get('file_parser', FileParser())
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def parser_auth(self):
        return self._parser_auth

    @parser_auth.setter
    def parser_auth(self, value):
        self._parser_auth = value

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    @property
    def file_parser(self):
        return self._file_parser

    @file_parser.setter
    def file_parser(self, value):
        self._file_parser = value

    def __call__(self):
        return self._parser

    def authorization_with_prefix(self, auth, name, file=None, key='name'):
        if file:
            with open(file) as f:
                attr = json.loads(f.read())[key]
            return authorization.with_prefix(attr, auth)
        return authorization.with_prefix(name, auth)

    def _build_access_token_argument(self):
        parser = self._parser_auth.add_parser('access', aliases=['access-token'], help='get access token', parents=[self._parent_parser()])
        parser.set_defaults(func=lambda args: print(mfa_with_pyotp.get_access_token(args)))

    def _build_verify_resource_file_argument(self):
        parser = self._parser_auth.add_parser('file', aliases=['verify-resource-file'], parents=[self._parent_parser(), self._file_parser()],
            help='verify user has authorization to access resource with prefix in file')
        parser.add_argument('-k', '--key', action='store', help='key of attribute with prefix to verify', required=False, default='name')
        parser.set_defaults(func=lambda args: print(self.authorization_with_prefix(args, None, file=args.file, key=args.key)))

    def _build_verify_resource_name_argument(self):
        parser = self._parser_auth.add_parser('name', aliases=['verify-resource-name'], parents=[self._parent_parser()],
            help='verify user has authorization to access resource with prefix in name')
        parser.add_argument('-n', '--name', help='name of resource with prefix to verify', required=True)
        parser.set_defaults(func=lambda args: print(self.authorization_with_prefix(args, args.name)))

    def _create_parser(self):
        self._build_access_token_argument()
        self._build_verify_resource_file_argument()
        self._build_verify_resource_name_argument()
