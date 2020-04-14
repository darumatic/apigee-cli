import argparse

from apigee.api.stats import Stats

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser
from apigee.parsers.silent_parser import SilentParser
from apigee.parsers.verbose_parser import VerboseParser

from apigee.util import console


class ParserStats:
    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_stats = self._parser.add_parser(
            "stats", help="access metrics collected by Apigee Edge"
        ).add_subparsers()
        self._parent_parser = kwargs.get("parent_parser", ParentParser())
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
    def parser_stats(self):
        return self._parser_stats

    @parser_stats.setter
    def parser_stats(self, value):
        self._parser_stats = value

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

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

    def _build_get_license_utilization_argument(self):
        parser = self._parser_stats.add_parser(
            "get-license-utilization",
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
            help="Gets current license utilization per environment.",
        )
        parser.add_argument(
            "-e",
            "--environments",
            help="list of environments",
            nargs="+",
            required=True,
        )
        parser.add_argument("--time-range", help="time range e.g. '01/01/2020 00:00~04/01/2020 00:00'", required=True)
        parser.add_argument("--tzo", help="tzo", type=int, default=None)
        parser.add_argument("--api-calls-per-year", help="Apigee license per year (API Calls). Default is 10,000,000,000.", type=int, default=10000000000)
        parser.set_defaults(
            func=lambda args: Stats(args, args.org).get_license_utilization(
                args.time_range, environments=args.environments, tzo=args.tzo, api_calls_per_year=args.api_calls_per_year
            )
        )

    def _create_parser(self):
        self._build_get_license_utilization_argument()
