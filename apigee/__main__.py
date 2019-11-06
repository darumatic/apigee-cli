#!/usr/bin/env python
"""apigee"""

import argparse

import apigee

from apigee.api import *

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.file_parser import FileParser
from apigee.parsers.dir_parser import DirParser
from apigee.parsers.format_parser import FormatParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser

from apigee.parsers.parser_apis import ParserApis
from apigee.parsers.parser_deployments import ParserDeployments
from apigee.parsers.parser_keyvaluemaps import ParserKeyvaluemaps
from apigee.parsers.parser_developers import ParserDevelopers
from apigee.parsers.parser_apps import ParserApps
from apigee.parsers.parser_apiproducts import ParserApiproducts
from apigee.parsers.parser_targetservers import ParserTargetservers
from apigee.parsers.parser_maskconfigs import ParserMaskconfigs
from apigee.parsers.parser_permissions import ParserPermissions
from apigee.parsers.parser_prepend import ParserPrepend

from apigee.util import *

@exception_handler
def main():
    parent_parser = ParentParser()
    file_parser = FileParser()
    dir_parser = DirParser()
    format_parser = FormatParser()
    environment_parser = EnvironmentParser()
    prefix_parser = PrefixParser(profile=parent_parser.profile)

    parser = argparse.ArgumentParser(prog=apigee.CMD, description=apigee.description)
    parser.add_argument('-V', '--version', action='version', version=apigee.APP + ' ' + apigee.__version__)
    subparsers = parser.add_subparsers()

    parser_test = subparsers.add_parser('test', aliases=['get-access-token'], help='test get access token', parents=[parent_parser()])
    parser_test.set_defaults(func=test)

    parser_configure = subparsers.add_parser('configure', help='configure credentials')
    parser_configure.add_argument('-P', '--profile', help='name of profile to create', default='default')
    parser_configure.set_defaults(func=config.main)

    # parser_apis = subparsers.add_parser('apis', help='apis').add_subparsers()
    subparsers = ParserApis(subparsers, parent_parser=parent_parser, dir_parser=dir_parser, environment_parser=environment_parser, prefix_parser=prefix_parser).parser
    # subparsers = ParserApis(subparsers).parser

    # parser_deployments = subparsers.add_parser('deployments', aliases=['deps'], help='see apis that are actively deployed').add_subparsers()
    subparsers = ParserDeployments(subparsers, parent_parser=parent_parser).parser

    # parser_keyvaluemaps = subparsers.add_parser('kvms', aliases=['keyvaluemaps'], help='keyvaluemaps').add_subparsers()
    subparsers = ParserKeyvaluemaps(subparsers, parent_parser=parent_parser, file_parser=file_parser, environment_parser=environment_parser, prefix_parser=prefix_parser).parser

    # parser_developers = subparsers.add_parser('developers', aliases=['devs'], help='developers').add_subparsers()
    subparsers = ParserDevelopers(subparsers, parent_parser=parent_parser, prefix_parser=prefix_parser).parser

    # parser_apps = subparsers.add_parser('apps', help='developer apps').add_subparsers()
    subparsers = ParserApps(subparsers, parent_parser=parent_parser, prefix_parser=prefix_parser).parser

    # parser_apiproducts = subparsers.add_parser('products', aliases=['prods'], help='api products').add_subparsers()
    subparsers = ParserApiproducts(subparsers, parent_parser=parent_parser, prefix_parser=prefix_parser).parser

    # parser_targetservers = subparsers.add_parser('ts', aliases=['targetservers'], help='target servers').add_subparsers()
    subparsers = ParserTargetservers(subparsers, parent_parser=parent_parser, file_parser=file_parser, environment_parser=environment_parser, prefix_parser=prefix_parser).parser

    # parser_maskconfigs = subparsers.add_parser('mask', aliases=['maskconfigs'], help='data masks').add_subparsers()
    subparsers = ParserMaskconfigs(subparsers, parent_parser=parent_parser).parser

    # parser_permissions = subparsers.add_parser('perms', aliases=['permissions'], help='manage permissions for a role').add_subparsers()
    subparsers = ParserPermissions(subparsers, parent_parser=parent_parser).parser

    # parser_prepend = subparsers.add_parser('prepend', aliases=['prefix'], help='prepend all matching strings with a prefix in all files in the specified directory (rudimentary stream editor). this is potentially VERY DANGEROUS. make sure you have version control such as Git to revert any changes in the target directory.', parents=[dir_parser()])
    # parser_prepend.add_argument('-P', '--prefix', help='prefix to prepend', required=True)
    # parser_prepend.add_argument('-r', '--resource', help='apigee resource to be prepended', required=True)
    # parser_prepend.set_defaults(func=prepend.main)
    subparsers = ParserPrepend(subparsers, dir_parser=dir_parser).parser

    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.error('too few arguments')
    func(args)

if __name__ == '__main__':
    main()
