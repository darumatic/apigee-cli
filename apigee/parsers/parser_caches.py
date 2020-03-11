import argparse

from apigee.api.caches import Caches

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.file_parser import FileParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser
from apigee.parsers.silent_parser import SilentParser
from apigee.parsers.verbose_parser import VerboseParser

from apigee.util import console


class ParserCaches:
    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_caches = self._parser.add_parser(
            "caches", help="manage caches"
        ).add_subparsers()
        self._parent_parser = kwargs.get("parent_parser", ParentParser())
        self._file_parser = kwargs.get("file_parser", FileParser())
        self._environment_parser = kwargs.get("environment_parser", EnvironmentParser())
        self._prefix_parser = kwargs.get(
            "prefix_parser", PrefixParser(profile="default")
        )
        self._silent_parser = kwargs.get("silent_parser", SilentParser())
        self._verbose_parser = kwargs.get("verbose_parser", VerboseParser())
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
        parser = self._parser_caches.add_parser(
            "clear",
            aliases=["clear-all-cache-entries"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Clears all cache entries.",
        )
        parser.add_argument("-n", "--name", help="name", required=True)
        parser.set_defaults(
            func=lambda args: console.log(
                Caches(args, args.org, args.name)
                .clear_all_cache_entries(args.environment)
                .text
            )
        )

    def _build_clear_a_cache_entry_argument(self):
        parser = self._parser_caches.add_parser(
            "clear-entry",
            aliases=["clear-a-cache-entry"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Clears a cache entry, which is identified by the full CacheKey prefix and value.",
        )
        parser.add_argument("-n", "--name", help="name", required=True)
        parser.add_argument("--entry", help="cache entry to clear", required=True)
        parser.set_defaults(
            func=lambda args: console.log(
                Caches(args, args.org, args.name)
                .clear_a_cache_entry(args.environment, args.entry)
                .text
            )
        )

    def _build_create_a_cache_in_an_environment_argument(self):
        parser = self._parser_caches.add_parser(
            "create",
            aliases=["create-a-cache-in-an-environment"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Creates a cache in an environment. Caches are created per environment. For data segregation, a cache created in 'test', for example, cannot be accessed by API proxies deployed in 'prod'. The JSON object in the request body can be empty to create a cache with the default settings.",
        )
        parser.add_argument("-n", "--name", help="name", required=True)
        parser.add_argument("-b", "--body", help="request body", required=True)
        parser.set_defaults(
            func=lambda args: console.log(
                Caches(args, args.org, args.name)
                .create_a_cache_in_an_environment(args.environment, args.body)
                .text
            )
        )

    def _build_get_information_about_a_cache_argument(self):
        parser = self._parser_caches.add_parser(
            "get",
            aliases=["get-information-about-a-cache"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Gets information about a cache. The response might contain a property named persistent. That property is no longer used by Edge.",
        )
        parser.add_argument("-n", "--name", help="name", required=True)
        parser.set_defaults(
            func=lambda args: console.log(
                Caches(args, args.org, args.name)
                .get_information_about_a_cache(args.environment)
                .text
            )
        )

    def _build_list_caches_in_an_environment_argument(self):
        parser = self._parser_caches.add_parser(
            "list",
            aliases=["list-caches-in-an-environment"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
                self._prefix_parser(),
            ],
            help="List caches in an environment.",
        )
        parser.set_defaults(
            func=lambda args: console.log(
                Caches(args, args.org, None).list_caches_in_an_environment(
                    args.environment, prefix=args.prefix
                )
            )
        )

    def _build_update_a_cache_in_an_environment_argument(self):
        parser = self._parser_caches.add_parser(
            "update",
            aliases=["update-a-cache-in-an-environment"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Updates a cache in an environment. You must specify the complete definition of the cache, including the properties that you want to change and the ones that retain their current value. Any properties omitted from the request body are reset to their default value. Use Get information about a cache to obtain an object containing the current value of all properties, then change only those that you want to update.",
        )
        parser.add_argument("-n", "--name", help="name", required=True)
        parser.add_argument("-b", "--body", help="request body", required=True)
        parser.set_defaults(
            func=lambda args: console.log(
                Caches(args, args.org, args.name)
                .update_a_cache_in_an_environment(args.environment, args.body)
                .text
            )
        )

    def _build_delete_a_cache_argument(self):
        parser = self._parser_caches.add_parser(
            "delete",
            aliases=["delete-a-cache"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Deletes a cache.",
        )
        parser.add_argument("-n", "--name", help="name", required=True)
        parser.set_defaults(
            func=lambda args: console.log(
                Caches(args, args.org, args.name).delete_a_cache(args.environment).text
            )
        )

    def _build_push_cache_argument(self):
        parser = self._parser_caches.add_parser(
            "push",
            aliases=["push-cache"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
                self._file_parser(),
            ],
            help="Push Cache to Apigee. This will create/update a Cache.",
        )
        parser.set_defaults(
            func=lambda args: Caches(args, args.org, None).push_cache(
                args.environment, args.file
            )
        )

    def _create_parser(self):
        self._build_clear_all_cache_entries_argument()
        self._build_clear_a_cache_entry_argument()
        self._build_create_a_cache_in_an_environment_argument()
        self._build_get_information_about_a_cache_argument()
        self._build_list_caches_in_an_environment_argument()
        self._build_update_a_cache_in_an_environment_argument()
        self._build_delete_a_cache_argument()
        self._build_push_cache_argument()
