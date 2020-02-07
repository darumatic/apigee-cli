import argparse

from apigee.api import deploy
from apigee.api.apis import Apis

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.dir_parser import DirParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser

class ParserApis:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_apis = self._parser.add_parser('apis', help='manage apis').add_subparsers()
        self._parent_parser = kwargs.get('parent_parser', ParentParser())
        self._dir_parser = kwargs.get('dir_parser', DirParser())
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
    def parser_apis(self):
        return self._parser_apis

    @parser_apis.setter
    def parser_apis(self, value):
        self._parser_apis = value

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

    def _build_apis_deploy_argument(self):
        apis_deploy = self._parser_apis.add_parser('deploy', help='deploy apis', parents=[self._parent_parser(), self._dir_parser(), self._environment_parser()])
        apis_deploy.add_argument('-n', '--name', help='name', required=True)
        # apis_deploy.add_argument('-d', '--directory', help='directory name')
        # apis_deploy.add_argument('-p', '--path', help='base path')
        apis_deploy.add_argument('-i', '--import-only', action='store_true', help='denotes to import only and not actually deploy')
        apis_deploy.add_argument('-s', '--seamless-deploy', action='store_true', help='seamless deploy the bundle')
        apis_deploy.set_defaults(func=deploy.deploy)

    def _build_delete_api_proxy_revision_argument(self):
        delete_api_proxy_revision = self._parser_apis.add_parser('delete-rev', aliases=['delete-api-proxy-revision', 'delete-revision'], parents=[self._parent_parser()],
            help='Deletes a revision of an API proxy and all policies, resources, endpoints, and revisions associated with it. The API proxy revision must be undeployed before you can delete it.')
        delete_api_proxy_revision.add_argument('-n', '--name', help='name', required=True)
        delete_api_proxy_revision.add_argument('-r', '--revision-number', type=int, help='revision number', required=True)
        delete_api_proxy_revision.set_defaults(func=lambda args: print(Apis(args, args.org, args.name).delete_api_proxy_revision(args.revision_number).text))

    def _build_delete_undeployed_revisions_argument(self):
        delete_undeployed_revisions = self._parser_apis.add_parser('clean', aliases=['delete-undeployed-revisions'], parents=[self._parent_parser()],
            help='Deletes all undeployed revisions of an API proxy and all policies, resources, endpoints, and revisions associated with it.')
        delete_undeployed_revisions.add_argument('-n', '--name', help='name', required=True)
        delete_undeployed_revisions.add_argument('--save-last', metavar='N', type=int, default=0, help='denotes not to delete the N most recent revisions', required=False)
        delete_undeployed_revisions.add_argument('--dry-run', action='store_true', help='show revisions to be deleted but do not delete', required=False)
        delete_undeployed_revisions.set_defaults(func=lambda args: Apis(args, args.org, args.name).delete_undeployed_revisions(save_last=args.save_last, dry_run=args.dry_run))

    def _build_export_api_proxy_argument(self):
        export_api_proxy = self._parser_apis.add_parser('export', aliases=['export-api-proxy'], parents=[self._parent_parser()],
            help='Outputs an API proxy revision as a ZIP formatted bundle of code and config files. This enables local configuration and development, including attachment of policies and scripts.')
        export_api_proxy.add_argument('-n', '--name', help='name', required=True)
        export_api_proxy.add_argument('-r', '--revision-number', type=int, help='revision number', required=True)
        export_api_proxy.add_argument('-O', '--output-file', help='output file')
        export_api_proxy.set_defaults(func=lambda args: Apis(args, args.org, args.name).export_api_proxy(args.revision_number, write=True, output_file=args.output_file if args.output_file else '{}.zip'.format(args.name)))
        # export_api_proxy.set_defaults(func=apis.export_api_proxy)

    def _build_pull_argument(self):
        pull_api = self._parser_apis.add_parser('pull', parents=[self._parent_parser(), self._environment_parser()],
            help='Pull API proxy revision as a ZIP formatted bundle along with KeyValueMap and TargetServer dependencies into the current working directory.')
        pull_api.add_argument('-n', '--name', help='name', required=True)
        pull_api.add_argument('-r', '--revision-number', type=int, help='revision number', required=True)
        pull_api.add_argument('-f', '--force', action='store_true', help='force write files')
        pull_api.add_argument('--work-tree', help='set the path to the working tree')
        pull_api.add_argument('--prefix', help='prefix to prepend. WARNING: this is not foolproof. make sure to review the changes.')
        pull_api.add_argument('-b', '--basepath', help='set default basepath in apiproxy/proxies/default.xml')
        pull_api.set_defaults(func=lambda args: Apis(args, args.org, args.name, args.revision_number, args.environment, work_tree=args.work_tree).pull(force=args.force, prefix=args.prefix, basepath=args.basepath))

    def _build_get_api_proxy_argument(self):
        get_api_proxy = self._parser_apis.add_parser('get', aliases=['get-api-proxy'], parents=[self._parent_parser()],
            help='Gets an API proxy by name, including a list of existing revisions of the proxy.')
        get_api_proxy.add_argument('-n', '--name', help='name', required=True)
        get_api_proxy.set_defaults(func=lambda args: print(Apis(args, args.org, args.name).get_api_proxy().text))

    def _build_list_api_proxies_argument(self):
        list_api_proxies = self._parser_apis.add_parser('list', aliases=['list-api-proxies'], parents=[self._parent_parser(), self._prefix_parser()],
            help='Gets the names of all API proxies in an organization. The names correspond to the names defined in the configuration files for each API proxy.')
        list_api_proxies.set_defaults(func=lambda args: print(Apis(args, args.org, None).list_api_proxies(prefix=args.prefix)))

    def _build_list_api_proxy_revisions_argument(self):
        list_api_proxies = self._parser_apis.add_parser('list-revs', aliases=['list-api-proxy-revisions', 'list-revisions'], parents=[self._parent_parser()],
            help='List all revisions for an API proxy.')
        list_api_proxies.add_argument('-n', '--name', help='name', required=True)
        list_api_proxies.set_defaults(func=lambda args: print(Apis(args, args.org, args.name).list_api_proxy_revisions().text))

    def _create_parser(self):
        self._build_apis_deploy_argument()
        self._build_delete_api_proxy_revision_argument()
        self._build_delete_undeployed_revisions_argument()
        self._build_export_api_proxy_argument()
        self._build_pull_argument()
        self._build_get_api_proxy_argument()
        self._build_list_api_proxies_argument()
        self._build_list_api_proxy_revisions_argument()
