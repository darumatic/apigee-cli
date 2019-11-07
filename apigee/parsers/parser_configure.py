import argparse

from apigee.util import config

class ParserConfigure:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    def __call__(self):
        return self._parser

    def _build_parser_configure_argument(self):
        parser_configure = self._parser.add_parser('configure', help='configure credentials')
        parser_configure.add_argument('-P', '--profile', help='name of profile to create', default='default')
        parser_configure.set_defaults(func=config.main)

    def _create_parser(self):
        self._build_parser_configure_argument()
