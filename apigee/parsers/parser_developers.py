import argparse

from apigee.api import developers

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.prefix_parser import PrefixParser

class ParserDevelopers:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_developers = self._parser.add_parser('developers', aliases=['devs'], help='developers').add_subparsers()
        self._parent_parser = kwargs.get('parent_parser', ParentParser())
        self._prefix_parser = kwargs.get('prefix_parser', PrefixParser(profile='default'))
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def parser_developers(self):
        return self._parser_developers

    @parser_developers.setter
    def parser_developers(self, value):
        self._parser_developers = value

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    @property
    def prefix_parser(self):
        return self._prefix_parser

    @prefix_parser.setter
    def prefix_parser(self, value):
        self._prefix_parser = value

    def __call__(self):
        return self._parser

    def _build_list_developers_argument(self):
        list_developers = self._parser_developers.add_parser('list', aliases=['list-developers'], parents=[self._parent_parser(), self._prefix_parser()],
            help='Lists all developers in an organization by email address. This call does not list any company developers who are a part of the designated organization.')
        list_developers.add_argument('--expand', action='store_true',
            help='Set to true to list developers exanded with details.')
        list_developers.add_argument('--count', default=1000, type=int,
            help='Limits the list to the number you specify. Use with the startKey parameter to provide more targeted filtering. The limit is 1000.')
        list_developers.add_argument('--startkey', default='',
            help='To filter the keys that are returned, enter the email of a developer that the list will start with.')
        list_developers.set_defaults(func=lambda args: print(developers.list_developers(args)))

    def _create_parser(self):
        self._build_list_developers_argument()
