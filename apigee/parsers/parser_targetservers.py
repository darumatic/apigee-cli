import argparse

from apigee.api.targetservers import Targetservers

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.file_parser import FileParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser

class ParserTargetservers:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_targetservers = self._parser.add_parser('targetservers', aliases=['ts'], help='manage target servers').add_subparsers()
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
    def parser_targetservers(self):
        return self._parser_targetservers

    @parser_targetservers.setter
    def parser_targetservers(self, value):
        self._parser_targetservers = value

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

    def _build_create_a_targetserver_argument(self):
        create_a_targetserver = self._parser_targetservers.add_parser('create', aliases=['create-a-targetserver'], parents=[self._parent_parser(), self._environment_parser()],
            help='Create a TargetServer in the specified environment. TargetServers are used to decouple TargetEndpoint HTTPTargetConnections from concrete URLs for backend services.')
        create_a_targetserver.add_argument('-b', '--body', help='request body', required=True)
        create_a_targetserver.set_defaults(func=lambda args: print(Targetservers(args, args.org, args.name).create_a_targetserver(args.environment, args.body).text))

    def _build_delete_a_targetserver_argument(self):
        delete_a_targetserver = self._parser_targetservers.add_parser('delete', aliases=['delete-a-targetserver'], parents=[self._parent_parser(), self._environment_parser()],
            help='Delete a TargetServer configuration from an environment. Returns information about the deleted TargetServer.')
        delete_a_targetserver.add_argument('-n', '--name', help='name', required=True)
        delete_a_targetserver.set_defaults(func=lambda args: print(Targetservers(args, args.org, args.name).delete_a_targetserver(args.environment).text))

    def _build_list_targetservers_in_an_environment_argument(self):
        list_targetservers_in_an_environment = self._parser_targetservers.add_parser('list', aliases=['list-targetservers-in-an-environment'], parents=[self._parent_parser(), self._environment_parser(), self._prefix_parser()],
            help='List all TargetServers in an environment.')
        list_targetservers_in_an_environment.set_defaults(func=lambda args: print(Targetservers(args, args.org, None).list_targetservers_in_an_environment(args.environment, prefix=args.prefix)))

    def _build_get_targetserver_argument(self):
        get_targetserver = self._parser_targetservers.add_parser('get', aliases=['get-targetserver'], parents=[self._parent_parser(), self._environment_parser()],
            help='Returns a TargetServer definition.')
        get_targetserver.add_argument('-n', '--name', help='name', required=True)
        get_targetserver.set_defaults(func=lambda args: print(Targetservers(args, args.org, args.name).get_targetserver(args.environment).text))

    def _build_update_a_targetserver_argument(self):
        update_a_targetserver = self._parser_targetservers.add_parser('update', aliases=['update-a-targetserver'], parents=[self._parent_parser(), self._environment_parser()],
            help='Modifies an existing TargetServer.')
        update_a_targetserver.add_argument('-n', '--name', help='name', required=True)
        update_a_targetserver.add_argument('-b', '--body', help='request body', required=True)
        update_a_targetserver.set_defaults(func=lambda args: print(Targetservers(args, args.org, args.name).update_a_targetserver(args.environment, args.body).text))

    def _build_push_targetserver_argument(self):
        push_targetserver = self._parser_targetservers.add_parser('push', aliases=['push-targetserver'], parents=[self._parent_parser(), self._environment_parser(), self._file_parser()],
            help='Push TargetServer to Apigee. This will create/update a TargetServer.')
        push_targetserver.set_defaults(func=lambda args: Targetservers(args, args.org, None).push_targetserver(args.environment, args.file))

    def _create_parser(self):
        self._build_create_a_targetserver_argument()
        self._build_delete_a_targetserver_argument()
        self._build_list_targetservers_in_an_environment_argument()
        self._build_get_targetserver_argument()
        self._build_update_a_targetserver_argument()
        self._build_push_targetserver_argument()
