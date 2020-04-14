import argparse

from apigee.api.sharedflows import Sharedflows

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.file_parser import FileParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser
from apigee.parsers.silent_parser import SilentParser
from apigee.parsers.verbose_parser import VerboseParser

from apigee.util import console
from apigee.util.types import ArgumentType


class ParserSharedflows:
    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_sharedflows = self._parser.add_parser(
            "sharedflows", aliases=["sf"], help="manage shared flows"
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
    def parser_sharedflows(self):
        return self._parser_sharedflows

    @parser_sharedflows.setter
    def parser_sharedflows(self, value):
        self._parser_sharedflows = value

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

    def _build_get_a_list_of_shared_flows_argument(self):
        parser = self._parser_sharedflows.add_parser(
            "list",
            aliases=["get-a-list-of-shared-flows"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._prefix_parser(),
            ],
            help="Gets an array of the names of shared flows in the organization. The response is a simple array of strings.",
        )
        parser.set_defaults(
            func=lambda args: console.log(
                Sharedflows(args, args.org).get_a_list_of_shared_flows(
                    prefix=args.prefix
                )
            )
        )

    def _build_import_a_shared_flow_argument(self):
        parser = self._parser_sharedflows.add_parser(
            "import",
            aliases=["import-a-shared-flow"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                # self._file_parser(),
            ],
            help="Uploads a ZIP-formatted shared flow configuration bundle from a local machine to an Edge organization. If the shared flow already exists, this creates a new revision of it. If the shared flow does not exist, this creates it. Once imported, the shared flow revision must be deployed before it can be accessed at runtime. By default, shared flow configurations are not validated on import.",
        )
        parser.add_argument(
            "-f",
            "--file",
            action="store",
            help="file path of the shared flow configuration in ZIP format",
            required=True,
            type=ArgumentType.isfile,
        )
        parser.add_argument("-n", "--name", help="shared flow name", required=True)
        parser.set_defaults(
            func=lambda args: console.log(
                Sharedflows(args, args.org)
                .import_a_shared_flow(args.file, args.name)
                .text
            )
        )

    def _build_export_a_shared_flow_argument(self):
        pass

    def _build_get_a_shared_flow_argument(self):
        parser = self._parser_sharedflows.add_parser(
            "get",
            aliases=["get-a-shared-flow"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
            help="Gets a shared flow by name, including a list of its revisions.",
        )
        parser.add_argument("-n", "--name", help="shared flow name", required=True)
        parser.set_defaults(
            func=lambda args: console.log(
                Sharedflows(args, args.org).get_a_shared_flow(args.name).text
            )
        )

    def _build_deploy_a_shared_flow_argument(self):
        parser = self._parser_sharedflows.add_parser(
            "deploy",
            aliases=["deploy-a-shared-flow"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                # self._file_parser(),
                self._environment_parser(),
            ],
            help="Deploys a shared flow revision to an environment in an organization. Shared flows cannot be used until they have been deployed to an environment. If you experience HTTP 500 errors during deployment, consider using the override parameter to deploy the shared flow in place of a revision currently deployed. The size limit of a shared flow bundle is 15 MB. WARNING: currently, --override does not seem to work on Apigee Edge. To counter this, existing shared flow revisions in the target environment will be undeployed before deploying a new revision, resulting in some downtime.",
        )
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "-f",
            "--file",
            action="store",
            help="file path of the shared flow configuration in ZIP format",
            # required=True,
            type=ArgumentType.isfile,
            default=None,
        )
        group.add_argument(
            "-r",
            "--revision-number",
            type=int,
            help="revision number",
            # required=True,
            default=None,
        )
        parser.add_argument("-n", "--name", help="shared flow name", required=True)
        parser.add_argument(
            "--override",
            action="store_true",
            help='Set this flag to "true" to deploy the shared flow revision in place of the revision currently deployed (also known as "zero downtime" deployment).',
        )
        parser.add_argument(
            "--delay",
            type=int,
            default=0,
            help="Enforces a delay, measured in seconds, before the currently deployed API proxy revision is undeployed and replaced by the new revision that is being deployed. Use this setting to minimize the impact of deployment on in-flight transactions. The default value is 0.",
        )
        parser.set_defaults(
            func=lambda args: console.log(
                Sharedflows(args, args.org)
                .deploy_a_shared_flow(
                    args.environment,
                    args.name,
                    args.revision_number,
                    override=args.override,
                    delay=args.delay,
                    shared_flow_file=args.file,
                )
                .text
            )
        )

    def _build_undeploy_a_shared_flow_argument(self):
        parser = self._parser_sharedflows.add_parser(
            "undeploy",
            aliases=["undeploy-a-shared-flow"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Undeploys a shared flow revision from an environment.",
        )
        parser.add_argument(
            "-r",
            "--revision-number",
            type=int,
            help="revision number",
            required=True,
            default=None,
        )
        parser.add_argument("-n", "--name", help="shared flow name", required=True)
        parser.set_defaults(
            func=lambda args: console.log(
                Sharedflows(args, args.org)
                .undeploy_a_shared_flow(
                    args.environment, args.name, args.revision_number,
                )
                .text
            )
        )

    def _build_get_deployment_environments_for_shared_flows_argument(self):
        parser = self._parser_sharedflows.add_parser(
            "get-deployment-environments",
            aliases=["get-deployment-environments-for-shared-flows"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
            help="Gets an array of the environments to which the shared flow is deployed.",
        )
        parser.add_argument("-n", "--name", help="shared flow name", required=True)
        parser.add_argument(
            "-r",
            "--revision-number",
            type=int,
            help="revision number",
            required=True,
            default=None,
        )
        parser.set_defaults(
            func=lambda args: console.log(
                Sharedflows(args, args.org)
                .get_deployment_environments_for_shared_flows(
                    args.name, args.revision_number
                )
                .text
            )
        )

    def _build_delete_a_shared_flow_argument(self):
        pass

    def _build_attach_a_shared_flow_to_a_flow_hook_argument(self):
        pass

    def _build_detaches_a_shared_flow_from_a_flow_hook_argument(self):
        pass

    def _build_get_the_shared_flow_attached_to_a_flow_hook_argument(self):
        parser = self._parser_sharedflows.add_parser(
            "get-flow-hook",
            aliases=["get-the-shared-flow-attached-to-a-flow-hook"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._environment_parser(),
            ],
            help="Returns the name of the shared flow attached to the specified flow hook. If there's no shared flow attached to the flow hook, the API does not return an error; it simply does not return a name in the response. Specify one of these flowhook locations in the API: PreProxyFlowHook, PreTargetFlowHook, PostTargetFlowHook, PostProxyFlowHook",
        )
        parser.add_argument(
            "--flow-hook",
            help="flow hook to which the shared flow is attached",
            required=True,
        )
        parser.set_defaults(
            func=lambda args: console.log(
                Sharedflows(args, args.org)
                .get_the_shared_flow_attached_to_a_flow_hook(
                    args.environment, args.flow_hook
                )
                .text
            )
        )

    def _build_get_shared_flow_deployments_argument(self):
        parser = self._parser_sharedflows.add_parser(
            "get-deployments",
            aliases=["get-shared-flow-deployments"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
            help="View all shared flow deployments.",
        )
        parser.add_argument("-n", "--name", help="shared flow name", required=True)
        parser.set_defaults(
            func=lambda args: console.log(
                Sharedflows(args, args.org).get_shared_flow_deployments(args.name).text
            )
        )

    def _build_get_shared_flow_revisions_argument(self):
        parser = self._parser_sharedflows.add_parser(
            "get-revisions",
            aliases=["get-shared-flow-revisions"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
            help="List the revisions of a shared flow.",
        )
        parser.add_argument("-n", "--name", help="shared flow name", required=True)
        parser.set_defaults(
            func=lambda args: console.log(
                Sharedflows(args, args.org).get_shared_flow_revisions(args.name).text
            )
        )

    def _create_parser(self):
        self._build_get_a_list_of_shared_flows_argument()
        self._build_import_a_shared_flow_argument()
        self._build_export_a_shared_flow_argument()
        self._build_get_a_shared_flow_argument()
        self._build_deploy_a_shared_flow_argument()
        self._build_undeploy_a_shared_flow_argument()
        self._build_get_deployment_environments_for_shared_flows_argument()
        self._build_delete_a_shared_flow_argument()
        self._build_attach_a_shared_flow_to_a_flow_hook_argument()
        self._build_detaches_a_shared_flow_from_a_flow_hook_argument()
        self._build_get_the_shared_flow_attached_to_a_flow_hook_argument()
        self._build_get_shared_flow_deployments_argument()
        self._build_get_shared_flow_revisions_argument()
