#!/usr/bin/env python
"""apigee"""

import argparse
import json

import apigee

from apigee.util import *

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.file_parser import FileParser
from apigee.parsers.dir_parser import DirParser
from apigee.parsers.format_parser import FormatParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser

from apigee.parsers.parser_authorization import ParserAuthorization
from apigee.parsers.parser_configure import ParserConfigure
from apigee.parsers.parser_apis import ParserApis
from apigee.parsers.parser_deployments import ParserDeployments
from apigee.parsers.parser_keyvaluemaps import ParserKeyvaluemaps
from apigee.parsers.parser_developers import ParserDevelopers
from apigee.parsers.parser_apps import ParserApps
from apigee.parsers.parser_apiproducts import ParserApiproducts
from apigee.parsers.parser_targetservers import ParserTargetservers
from apigee.parsers.parser_maskconfigs import ParserMaskconfigs
from apigee.parsers.parser_permissions import ParserPermissions
from apigee.parsers.parser_userroles import ParserUserroles
from apigee.parsers.parser_caches import ParserCaches

# from apigee.util import mfa_with_pyotp
from apigee.util.exceptions import exception_handler

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

    # parser_test = subparsers.add_parser('test', aliases=['access-token'], help='get access token', parents=[parent_parser()])
    # parser_test.set_defaults(func=lambda args: print(mfa_with_pyotp.get_access_token(args)))

    ParserAuthorization(subparsers).parser
    ParserConfigure(subparsers).parser
    ParserApis(subparsers, parent_parser=parent_parser, dir_parser=dir_parser, environment_parser=environment_parser, prefix_parser=prefix_parser).parser
    ParserDeployments(subparsers, parent_parser=parent_parser).parser
    ParserKeyvaluemaps(subparsers, parent_parser=parent_parser, file_parser=file_parser, environment_parser=environment_parser, prefix_parser=prefix_parser).parser
    ParserDevelopers(subparsers, parent_parser=parent_parser, prefix_parser=prefix_parser).parser
    ParserApps(subparsers, parent_parser=parent_parser, prefix_parser=prefix_parser).parser
    ParserApiproducts(subparsers, parent_parser=parent_parser, prefix_parser=prefix_parser).parser
    ParserTargetservers(subparsers, parent_parser=parent_parser, file_parser=file_parser, environment_parser=environment_parser, prefix_parser=prefix_parser).parser
    ParserMaskconfigs(subparsers, parent_parser=parent_parser).parser
    ParserPermissions(subparsers, parent_parser=parent_parser).parser
    ParserUserroles(subparsers, parent_parser=parent_parser).parser
    ParserCaches(subparsers, parent_parser=parent_parser, file_parser=file_parser, environment_parser=environment_parser, prefix_parser=prefix_parser).parser

    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.error('too few arguments')
    func(args)

if __name__ == '__main__':
    main()
