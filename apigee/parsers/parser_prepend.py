import argparse

from apigee.util import prepend

from apigee.parsers.dir_parser import DirParser

class ParserPrepend:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._dir_parser = kwargs.get('dir_parser', DirParser())
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def dir_parser(self):
        return self._dir_parser

    @dir_parser.setter
    def dir_parser(self, value):
        self._dir_parser = value

    def __call__(self):
        return self._parser

    def _build_parser_prepend_argument(self):
        parser_prepend = self._parser.add_parser('prepend', aliases=['prefix'], help='prepend all matching strings with a prefix in all files in the specified directory (rudimentary stream editor). this is potentially VERY DANGEROUS. make sure you have version control such as Git to revert any changes in the target directory.', parents=[self._dir_parser()])
        parser_prepend.add_argument('-P', '--prefix', help='prefix to prepend', required=True)
        parser_prepend.add_argument('-r', '--resource', help='apigee resource to be prepended', required=True)
        parser_prepend.set_defaults(func=prepend.main)

    def _create_parser(self):
        self._build_parser_prepend_argument()
