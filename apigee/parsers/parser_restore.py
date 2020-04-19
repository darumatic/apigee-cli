import argparse

from apigee.api import backup_and_restore as bar

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser
from apigee.parsers.silent_parser import SilentParser
from apigee.parsers.verbose_parser import VerboseParser

from apigee.util import console
from apigee.util.authorization import gen_auth
from apigee.util.os import read_file


class ParserRestore:
    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parent_parser = kwargs.get("parent_parser", ParentParser())
        self._environment_parser = kwargs.get("environment_parser", EnvironmentParser())
        self._prefix_parser = kwargs.get(
            "prefix_parser", PrefixParser(profile="default")
        )
        self._silent_parser = kwargs.get("silent_parser", SilentParser())
        self._verbose_parser = kwargs.get("verbose_parser", VerboseParser())
        self._parser_restore = self._parser.add_parser(
            "restore", help="restore specific resources from backup",
        ).add_subparsers()
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def parser_restore(self):
        return self._parser_restore

    @parser_restore.setter
    def parser_restore(self, value):
        self._parser_restore = value

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

    def _build_restore_kvms_argument(self):
        parser = self._parser_restore.add_parser(
            "keyvaluemaps",
            aliases=["kvms"],
            help="",
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
        )
        parser.add_argument(
            "--environments", help="list of environments", required=True
        )
        parser.add_argument(
            "-d", "--directory", help="directory of key value maps", required=True
        )
        parser.add_argument(
            "--snapshot-file", help="key value maps snapshot file", required=True
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="check which key value maps will be restored",
        )
        parser.set_defaults(
            func=lambda args: bar.restore_kvms(
                gen_auth(args.username, args.password, args.mfa_secret),
                args.org,
                args.environments,
                args.directory,
                snapshot=read_file(args.snapshot_file),
                dry_run=args.dry_run,
            )
        )

    def _build_restore_targetservers_argument(self):
        parser = self._parser_restore.add_parser(
            "targetservers",
            aliases=["ts"],
            help="",
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
        )
        parser.add_argument("--environment", help="list of environments", required=True)
        parser.add_argument(
            "-d", "--directory", help="directory of target servers", required=True
        )
        parser.add_argument(
            "--snapshot-file", help="target servers snapshot file", required=True
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="check which target servers will be restored",
        )
        parser.set_defaults(
            func=lambda args: bar.restore_targetservers(
                gen_auth(args.username, args.password, args.mfa_secret),
                args.org,
                args.environment,
                args.directory,
                snapshot=read_file(args.snapshot_file),
                dry_run=args.dry_run,
            )
        )

    def _build_restore_caches_argument(self):
        parser = self._parser_restore.add_parser(
            "caches",
            help="",
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
        )
        parser.add_argument("--environment", help="list of environments", required=True)
        parser.add_argument(
            "-d", "--directory", help="directory of caches", required=True
        )
        parser.add_argument(
            "--snapshot-file", help="caches snapshot file", required=True
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="check which caches will be restored",
        )
        parser.set_defaults(
            func=lambda args: bar.restore_caches(
                gen_auth(args.username, args.password, args.mfa_secret),
                args.org,
                args.environment,
                args.directory,
                snapshot=read_file(args.snapshot_file),
                dry_run=args.dry_run,
            )
        )

    def _build_restore_developers_argument(self):
        parser = self._parser_restore.add_parser(
            "developers",
            aliases=["devs"],
            help="",
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
        )
        parser.add_argument(
            "-d", "--directory", help="directory of developers", required=True
        )
        parser.add_argument(
            "--snapshot-file", help="developers snapshot file", required=True
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="check which developers will be restored",
        )
        parser.set_defaults(
            func=lambda args: bar.restore_developers(
                gen_auth(args.username, args.password, args.mfa_secret),
                args.org,
                args.directory,
                snapshot=read_file(args.snapshot_file),
                dry_run=args.dry_run,
            )
        )

    def _build_restore_products_argument(self):
        parser = self._parser_restore.add_parser(
            "apiproducts",
            aliases=["products"],
            help="",
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
        )
        parser.add_argument(
            "-d", "--directory", help="directory of API products", required=True
        )
        parser.add_argument(
            "--snapshot-file", help="API products snapshot file", required=True
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="check which API products will be restored",
        )
        parser.set_defaults(
            func=lambda args: bar.restore_products(
                gen_auth(args.username, args.password, args.mfa_secret),
                args.org,
                args.directory,
                snapshot=read_file(args.snapshot_file),
                dry_run=args.dry_run,
            )
        )

    def _build_restore_apps_argument(self):
        parser = self._parser_restore.add_parser(
            "apps",
            help="",
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
        )
        parser.add_argument(
            "-d", "--directory", help="directory of developer apps", required=True
        )
        parser.add_argument(
            "--snapshot-dir", help="developer apps snapshot directory", required=True
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="check which developer apps will be restored",
        )
        parser.set_defaults(
            func=lambda args: bar.restore_apps(
                gen_auth(args.username, args.password, args.mfa_secret),
                args.org,
                args.directory,
                args.snapshot_dir,
                dry_run=args.dry_run,
            )
        )

    def _build_restore_roles_argument(self):
        parser = self._parser_restore.add_parser(
            "userroles",
            aliases=["roles"],
            help="",
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
        )
        parser.add_argument(
            "-d", "--directory", help="directory of developer apps", required=True
        )
        parser.add_argument(
            "--snapshot-file", help="developer apps snapshot file", required=True
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="check which developer apps will be restored",
        )
        parser.set_defaults(
            func=lambda args: bar.restore_roles(
                gen_auth(args.username, args.password, args.mfa_secret),
                args.org,
                args.directory,
                snapshot=read_file(args.snapshot_file),
                dry_run=args.dry_run,
            )
        )

    def _create_parser(self):
        self._build_restore_kvms_argument()
        self._build_restore_targetservers_argument()
        self._build_restore_caches_argument()
        self._build_restore_developers_argument()
        self._build_restore_products_argument()
        self._build_restore_apps_argument()
        self._build_restore_roles_argument()
