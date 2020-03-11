import argparse

from apigee.api.debugsessions import Debugsessions

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.dir_parser import DirParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser
from apigee.parsers.silent_parser import SilentParser
from apigee.parsers.verbose_parser import VerboseParser

from apigee.util import console


class ParserDebugsessions:
    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_debugsessions = self._parser.add_parser(
            "debug",
            aliases=["trace", "debugsessions"],
            help="manage sessions configured in Apigee Edge to record specified messages and associated pipeline processing metadata for debugging purposes",
        ).add_subparsers()
        self._parent_parser = kwargs.get("parent_parser", ParentParser())
        self._dir_parser = kwargs.get("dir_parser", DirParser())
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
    def parser_debugsessions(self):
        return self._parser_debugsessions

    @parser_debugsessions.setter
    def parser_debugsessions(self, value):
        self._parser_debugsessions = value

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    @property
    def dir_parser(self):
        return self._dir_parser

    @dir_parser.setter
    def dir_parser(self, value):
        self._dir_parser = value

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

    def _build_create_a_debug_session_argument(self):
        parser = self._parser_debugsessions.add_parser(
            "create",
            aliases=["create-a-debug-session"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Create a debug session.",
        )
        parser.add_argument("-n", "--name", help="name", required=True)
        parser.add_argument(
            "-r", "--revision-number", help="the API revision number", required=True
        )
        parser.add_argument(
            "--session-name",
            help="the user-given name of the debug session (used to retrieve the results after debugging completes)",
            required=True,
        )
        parser.add_argument(
            "--timeout",
            help="the time in seconds after which the particular session should be discarded. Default is 600 seconds",
            default=600,
        )
        parser.add_argument(
            "--filter",
            help="query parameters that begin with either header_ or qparam_ to indicate a header or query parameter to filter",
            default="",
        )
        parser.set_defaults(
            func=lambda args: console.log(
                Debugsessions(args, args.org)
                .create_a_debug_session(
                    args.environment,
                    args.name,
                    args.revision_number,
                    args.session_name,
                    timeout=args.timeout,
                    filter=args.filter,
                )
                .text
            )
        )

    def _build_delete_debug_session_argument(self):
        parser = self._parser_debugsessions.add_parser(
            "delete",
            aliases=["delete-debug-session"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Deletes a debug session.",
        )
        parser.add_argument("-n", "--name", help="name", required=True)
        parser.add_argument(
            "-r", "--revision-number", help="the API revision number", required=True
        )
        parser.add_argument(
            "--session-name",
            help="the user-given name of the debug session",
            required=True,
        )
        parser.set_defaults(
            func=lambda args: console.log(
                Debugsessions(args, args.org)
                .delete_debug_session(
                    args.environment, args.name, args.revision_number, args.session_name
                )
                .text
            )
        )

    def _build_list_debug_sessions_argument(self):
        parser = self._parser_debugsessions.add_parser(
            "list",
            aliases=["list-debug-sessions"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="List all debug sessions created by the Create Debugsessions Session API call or by the Trace tool in the Edge management UI.",
        )
        parser.add_argument("-n", "--name", help="name", required=True)
        parser.add_argument(
            "-r", "--revision-number", help="the API revision number", required=True
        )
        parser.set_defaults(
            func=lambda args: console.log(
                Debugsessions(args, args.org)
                .list_debug_sessions(args.environment, args.name, args.revision_number)
                .text
            )
        )

    def _build_get_debug_session_transaction_IDs_argument(self):
        parser = self._parser_debugsessions.add_parser(
            "get-ids",
            aliases=["get-debug-session-transaction-IDs"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Retrieves a list of transaction IDs for a debug session that was created by the Create Debugsessions Session API call or by the Trace tool in the Edge management UI.",
        )
        parser.add_argument("-n", "--name", help="name", required=True)
        parser.add_argument(
            "-r", "--revision-number", help="the API revision number", required=True
        )
        parser.add_argument(
            "--session-name",
            help="the user-given name of the debug session",
            required=True,
        )
        parser.set_defaults(
            func=lambda args: console.log(
                Debugsessions(args, args.org)
                .get_debug_session_transaction_IDs(
                    args.environment, args.name, args.revision_number, args.session_name
                )
                .text
            )
        )

    def _build_get_debug_session_transaction_data_argument(self):
        parser = self._parser_debugsessions.add_parser(
            "get",
            aliases=["get-debug-session-transaction-data"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Get debug session transaction data.",
        )
        parser.add_argument("-n", "--name", help="name", required=True)
        parser.add_argument(
            "-r", "--revision-number", help="the API revision number", required=True
        )
        parser.add_argument(
            "--session-name",
            help="the user-given name of the debug session",
            required=True,
        )
        parser.add_argument(
            "--transaction-id", help="the ID of a debug transaction", required=True
        )
        parser.set_defaults(
            func=lambda args: console.log(
                Debugsessions(args, args.org)
                .get_debug_session_transaction_data(
                    args.environment,
                    args.name,
                    args.revision_number,
                    args.session_name,
                    args.transaction_id,
                )
                .text
            )
        )

    def _create_parser(self):
        self._build_create_a_debug_session_argument()
        self._build_delete_debug_session_argument()
        self._build_list_debug_sessions_argument()
        self._build_get_debug_session_transaction_IDs_argument()
        self._build_get_debug_session_transaction_data_argument()
