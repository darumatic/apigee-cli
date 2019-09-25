import argparse

from apigee.api.deployments import Deployments

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.silent_parser import SilentParser
from apigee.parsers.verbose_parser import VerboseParser

from apigee.util import console


class ParserDeployments:
    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_deployments = self._parser.add_parser(
            "deployments", aliases=["deps"], help="see API deployments"
        ).add_subparsers()
        self._parent_parser = kwargs.get("parent_parser", ParentParser())
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
    def parser_deployments(self):
        return self._parser_deployments

    @parser_deployments.setter
    def parser_deployments(self, value):
        self._parser_deployments = value

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    def __call__(self):
        return self._parser

    def _build_get_api_proxy_deployment_details_argument(self):
        get_api_proxy_deployment_details = self._parser_deployments.add_parser(
            "get",
            aliases=["get-api-proxy-deployment-details"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
            help="Returns detail on all deployments of the API proxy for all environments. All deployments are listed in the test and prod environments, as well as other environments, if they exist.",
        )
        get_api_proxy_deployment_details.add_argument(
            "-n", "--name", help="name", required=True
        )
        get_api_proxy_deployment_details.add_argument(
            "-r", "--revision-name", action="store_true", help="get revisions only"
        )
        get_api_proxy_deployment_details.add_argument(
            "-j",
            "--json",
            action="store_const",
            const="json",
            help="use json output",
            default="table",
        )
        # get_api_proxy_deployment_details.add_argument('--max-colwidth', help='max column width', type=int, default=40)
        get_api_proxy_deployment_details.add_argument(
            "--showindex", action="store_true", help="add row indices"
        )
        get_api_proxy_deployment_details.add_argument(
            "--tablefmt",
            help="defines how the table is formatted",
            default="plain",
            choices=(
                "plain",
                "simple",
                "github",
                "grid",
                "fancy_grid",
                "pipe",
                "orgtbl",
                "jira",
                "presto",
                "psql",
                "rst",
                "mediawiki",
                "moinmoin",
                "youtrack",
                "html",
                "latex",
                "latex_raw",
                "latex_booktabs",
                "textile",
            ),
            type=str,
        )
        get_api_proxy_deployment_details.set_defaults(
            func=lambda args: console.log(
                Deployments(args, args.org, args.name).get_api_proxy_deployment_details(
                    formatted=True,
                    format=args.json,
                    showindex=args.showindex,
                    tablefmt=args.tablefmt,
                    revision_name_only=args.revision_name,
                )
            )
        )

    def _create_parser(self):
        self._build_get_api_proxy_deployment_details_argument()
