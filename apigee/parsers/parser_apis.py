import argparse

from apigee.api import apis
from apigee.api import deploy

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.dir_parser import DirParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser

class ParserApis:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_apis = self._parser.add_parser('apis', help='apis').add_subparsers()
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

    def _build_export_api_proxy_argument(self):
        export_api_proxy = self._parser_apis.add_parser('export', aliases=['export-api-proxy'], parents=[self._parent_parser()],
            help='Outputs an API proxy revision as a ZIP formatted bundle of code and config files. This enables local configuration and development, including attachment of policies and scripts.')
        export_api_proxy.add_argument('-n', '--name', help='name', required=True)
        export_api_proxy.add_argument('-r', '--revision-number', help='revision number', required=True)
        export_api_proxy.add_argument('-O', '--output-file', help='output file')
        # export_api_proxy.set_defaults(func=lambda args: print(apis.export_api_proxy(args).text))
        export_api_proxy.set_defaults(func=apis.export_api_proxy)

    def _build_get_api_proxy_argument(self):
        get_api_proxy = self._parser_apis.add_parser('get', aliases=['get-api-proxy'], parents=[self._parent_parser()],
            help='Gets an API proxy by name, including a list of existing revisions of the proxy.')
        get_api_proxy.add_argument('-n', '--name', help='name', required=True)
        get_api_proxy.set_defaults(func=lambda args: print(apis.get_api_proxy(args).text))

    def _build_list_api_proxies_argument(self):
        list_api_proxies = self._parser_apis.add_parser('list', aliases=['list-api-proxies'], parents=[self._parent_parser(), self._prefix_parser()],
            help='Gets the names of all API proxies in an organization. The names correspond to the names defined in the configuration files for each API proxy.')
        list_api_proxies.set_defaults(func=lambda args: print(apis.list_api_proxies(args)))

    def _create_parser(self):
        self._build_apis_deploy_argument()
        self._build_export_api_proxy_argument()
        self._build_get_api_proxy_argument()
        self._build_list_api_proxies_argument()
