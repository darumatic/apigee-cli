import argparse

from apigee.api.backup import Backup

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser
from apigee.parsers.silent_parser import SilentParser
from apigee.parsers.verbose_parser import VerboseParser

from apigee.util import console
from apigee.util.authorization import gen_auth


class ParserBackup:
    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parent_parser = kwargs.get("parent_parser", ParentParser())
        self._environment_parser = kwargs.get("environment_parser", EnvironmentParser())
        self._prefix_parser = kwargs.get(
            "prefix_parser", PrefixParser(profile="default")
        )
        self._silent_parser = kwargs.get("silent_parser", SilentParser())
        self._verbose_parser = kwargs.get("verbose_parser", VerboseParser())
        self._parser_backup = self._parser.add_parser(
            "backup",
            help="Downloads Apigee Edge configuration files for API proxies, key value maps, target servers, caches, developers, API products, developer apps, and user roles (including permissions and associated users).",
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._prefix_parser(),
            ],
        )
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def parser_backup(self):
        return self._parser_backup

    @parser_backup.setter
    def parser_backup(self, value):
        self._parser_backup = value

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

    def _build_backup_argument(self):
        self._parser_backup.add_argument(
            "--environments", nargs="+", help="list of environments", required=True
        )
        self._parser_backup.add_argument(
            "--target-directory", help="target directory", default=None
        )
        self._parser_backup.add_argument(
            "--resources",
            nargs="+",
            choices=(
                "apis",
                "keyvaluemaps",
                "targetservers",
                "caches",
                "developers",
                "apiproducts",
                "apps",
                "userroles",
            ),
            help="resources to back up. default is all.",
            default=None,
        )
        self._parser_backup.set_defaults(
            func=lambda args: Backup(
                gen_auth(args.username, args.password, args.mfa_secret,),
                args.org,
                target_directory=args.target_directory,
            ).backup(
                environments=args.environments,
                prefix=args.prefix,
                fs_write=True,
                resources=args.resources,
            )
        )

    def _create_parser(self):
        self._build_backup_argument()
