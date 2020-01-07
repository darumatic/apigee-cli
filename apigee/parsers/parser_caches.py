import argparse

from apigee.api.caches import Caches

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.file_parser import FileParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser

class ParserCaches:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_caches = self._parser.add_parser('caches', help='manage caches').add_subparsers()
        self._parent_parser = kwargs.get('parent_parser', ParentParser())
        self._file_parser = kwargs.get('file_parser', FileParser())
        self._environment_parser = kwargs.get('environment_parser', EnvironmentParser())
        self._prefix_parser = kwargs.get('prefix_parser', PrefixParser(profile='default'))
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def parser_caches(self):
        return self._parser_caches

    @parser_caches.setter
    def parser_caches(self, value):
        self._parser_caches = value

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

    @property
    def environment_parser(self):
        return self._environment_parser

    @environment_parser.setter
    def environment_parser(self, value):
        self._environment_parser = value

    @property
    def prefix_parser(self):
        return self._prefix_parser

    @prefix_parser.setter
    def prefix_parser(self, value):
        self._prefix_parser = value

    def __call__(self):
        return self._parser

    def _build_clear_all_cache_entries_argument(self):
        parser = self._parser_caches.add_parser('clear', aliases=['clear-all-cache-entries'], parents=[self._parent_parser(), self._environment_parser()],
            help='Clears all cache entries.')
        parser.add_argument('-n', '--name', help='name', required=True)
        parser.set_defaults(func=lambda args: print(Caches(args, args.org, args.name).clear_all_cache_entries(args.environment).text))

    def _build_clear_a_cache_entry_argument(self):
        parser = self._parser_caches.add_parser('clear-entry', aliases=['clear-a-cache-entry'], parents=[self._parent_parser(), self._environment_parser()],
            help='Clears a cache entry, which is identified by the full CacheKey prefix and value.')
        parser.add_argument('-n', '--name', help='name', required=True)
        parser.add_argument('--entry', help='cache entry to clear', required=True)
        parser.set_defaults(func=lambda args: print(Caches(args, args.org, args.name).clear_a_cache_entry(args.environment, args.entry).text))

    def _create_parser(self):
        self._build_clear_all_cache_entries_argument()
        self._build_clear_a_cache_entry_argument()
