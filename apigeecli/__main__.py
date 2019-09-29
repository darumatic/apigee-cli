#!/usr/bin/env python
"""apigeecli"""

import argparse
import os
import sys

import apigeecli

from apigeecli import APIGEE_ORG
from apigeecli import APIGEE_USERNAME
from apigeecli import APIGEE_PASSWORD
from apigeecli import APIGEE_MFA_SECRET
from apigeecli.api import *
from apigeecli.util import *

@exception_handler
def main():
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--mfa-secret', action='store', help='apigee mfa secret', required=False, default=APIGEE_MFA_SECRET)

    if APIGEE_ORG is None:
        parent_parser.add_argument('-o', '--org', action='store', help='apigee org', required=True)
    else:
        parent_parser.add_argument('-o', '--org', action='store', help='apigee org', required=False, default=APIGEE_ORG)
    if APIGEE_USERNAME is None:
        parent_parser.add_argument('-u', '--username', action='store', help='apigee username', required=True)
    else:
        parent_parser.add_argument('-u', '--username', action='store', help='apigee username', required=False, default=APIGEE_USERNAME)
    if APIGEE_PASSWORD is None:
        parent_parser.add_argument('-p', '--password', action='store', help='apigee password', required=True)
    else:
        parent_parser.add_argument('-p', '--password', action='store', help='apigee password', required=False, default=APIGEE_PASSWORD)

    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument('-f', '--file', action='store', help='file path', required=True, type=isfile)

    dir_parser = argparse.ArgumentParser(add_help=False)
    dir_parser.add_argument('-d', '--directory', action='store', help='directory path', required=True, type=isdir)

    environment_parser = argparse.ArgumentParser(add_help=False)
    environment_parser.add_argument('-e', '--environment', help='environment', required=True)

    parser = argparse.ArgumentParser(prog=apigeecli.APP, description=apigeecli.description)
    parser.add_argument('--version', action='version', version=apigeecli.APP + ' ' + apigeecli.__version__)
    subparsers = parser.add_subparsers()

    parser_test = subparsers.add_parser('test', help='test get access token', parents=[parent_parser])
    parser_test.set_defaults(func=test)

    parser_apis = subparsers.add_parser('apis', help='apis').add_subparsers()
    parser_deployments = subparsers.add_parser('deployments', help='see apis that are actively deployed').add_subparsers()
    parser_keyvaluemaps = subparsers.add_parser('keyvaluemaps', help='keyvaluemaps').add_subparsers()

    apis_deploy = parser_apis.add_parser('deploy', help='deploy apis', parents=[parent_parser, dir_parser, environment_parser])
    apis_deploy.add_argument('-n', '--name', help='name', required=True)
    # apis_deploy.add_argument('-d', '--directory', help='directory name')
    # apis_deploy.add_argument('-p', '--path', help='base path')
    apis_deploy.add_argument('-i', '--import-only', action='store_true', help='denotes to import only and not actually deploy')
    apis_deploy.add_argument('-s', '--seamless-deploy', action='store_true', help='seamless deploy the bundle')
    apis_deploy.set_defaults(func=deploy.deploy)

    # apis_list = parser_apis.add_parser('list', help='list apis', parents=[parent_parser])

    export_api_proxy = parser_apis.add_parser('export', aliases=['export-api-proxy'], parents=[parent_parser],
        help='Outputs an API proxy revision as a ZIP formatted bundle of code and config files. This enables local configuration and development, including attachment of policies and scripts.')
    export_api_proxy.add_argument('-n', '--name', help='name', required=True)
    export_api_proxy.add_argument('-r', '--revision-number', help='revision number', required=True)
    export_api_proxy.add_argument('-O', '--output-file', help='output file')
    # export_api_proxy.set_defaults(func=lambda args: print(apis.export_api_proxy(args).text))
    export_api_proxy.set_defaults(func=apis.export_api_proxy)

    get_api_proxy = parser_apis.add_parser('get', aliases=['get-api-proxy'], parents=[parent_parser],
        help='Gets an API proxy by name, including a list of existing revisions of the proxy.')
    get_api_proxy.add_argument('-n', '--name', help='name', required=True)
    get_api_proxy.set_defaults(func=lambda args: print(apis.get_api_proxy(args).text))

    list_api_proxies = parser_apis.add_parser('list', aliases=['list-api-proxies'], parents=[parent_parser],
        help='Gets the names of all API proxies in an organization. The names correspond to the names defined in the configuration files for each API proxy.')
    list_api_proxies.set_defaults(func=lambda args: print(apis.list_api_proxies(args).text))

    get_api_proxy_deployment_details = parser_deployments.add_parser('get', aliases=['get-api-proxy-deployment-details'], parents=[parent_parser],
        help='Returns detail on all deployments of the API proxy for all environments. All deployments are listed in the test and prod environments, as well as other environments, if they exist.')
    get_api_proxy_deployment_details.add_argument('-n', '--name', help='name', required=True)
    get_api_proxy_deployment_details.add_argument('-r', '--revision-name', action='store_true', help='get revisions only')
    get_api_proxy_deployment_details.set_defaults(func=lambda args: print(deployments.get_api_proxy_deployment_details(args)))

    create_keyvaluemap_in_an_environment = parser_keyvaluemaps.add_parser('create', aliases=['create-keyvaluemap-in-an-environment'], parents=[parent_parser, environment_parser],
        help='Creates a key value map in an environment.')
    create_keyvaluemap_in_an_environment.add_argument('-n', '--name', help='name', required=True)
    create_keyvaluemap_in_an_environment.add_argument('-b', '--body', help='request body', required=True)
    create_keyvaluemap_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.create_keyvaluemap_in_an_environment(args).text))

    delete_keyvaluemap_from_an_environment = parser_keyvaluemaps.add_parser('delete', aliases=['delete-keyvaluemap-from-an-environment'], parents=[parent_parser, environment_parser],
        help='Deletes a key/value map and all associated entries from an environment.')
    delete_keyvaluemap_from_an_environment.add_argument('-n', '--name', help='name', required=True)
    delete_keyvaluemap_from_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.delete_keyvaluemap_from_an_environment(args).text))

    delete_keyvaluemap_entry_in_an_environment = parser_keyvaluemaps.add_parser('delete-entry', aliases=['delete-keyvaluemap-entry-in-an-environment'], parents=[parent_parser, environment_parser],
        help='Deletes a specific key/value map entry in an environment by name, along with associated entries.')
    delete_keyvaluemap_entry_in_an_environment.add_argument('-n', '--name', help='name', required=True)
    delete_keyvaluemap_entry_in_an_environment.add_argument('--entry-name', help='entry name', required=True)
    delete_keyvaluemap_entry_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.delete_keyvaluemap_entry_in_an_environment(args).text))

    get_keyvaluemap_in_an_environment = parser_keyvaluemaps.add_parser('get', aliases=['get-keyvaluemap-in-an-environment'], parents=[parent_parser, environment_parser],
        help='Gets a KeyValueMap (KVM) in an environment by name, along with the keys and values.')
    get_keyvaluemap_in_an_environment.add_argument('-n', '--name', help='name', required=True)
    get_keyvaluemap_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.get_keyvaluemap_in_an_environment(args).text))

    get_a_keys_value_in_an_environment_scoped_keyvaluemap = parser_keyvaluemaps.add_parser('get-value', aliases=['get-a-keys-value-in-an-environment-scoped-keyvaluemap'], parents=[parent_parser, environment_parser],
        help='Gets the value of a key in an environment-scoped KeyValueMap (KVM).')
    get_a_keys_value_in_an_environment_scoped_keyvaluemap.add_argument('-n', '--name', help='name', required=True)
    get_a_keys_value_in_an_environment_scoped_keyvaluemap.add_argument('--entry-name', help='entry name', required=True)
    get_a_keys_value_in_an_environment_scoped_keyvaluemap.set_defaults(func=lambda args: print(keyvaluemaps.get_a_keys_value_in_an_environment_scoped_keyvaluemap(args).text))

    list_keyvaluemaps_in_an_environment = parser_keyvaluemaps.add_parser('list', aliases=['list-keyvaluemaps-in-an-environment'], parents=[parent_parser, environment_parser],
        help='Lists the name of all key/value maps in an environment and optionally returns an expanded view of all key/value maps for the environment.')
    list_keyvaluemaps_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.list_keyvaluemaps_in_an_environment(args).text))

    update_keyvaluemap_in_an_environment = parser_keyvaluemaps.add_parser('update', aliases=['update-keyvaluemap-in-an-environment'], parents=[parent_parser, environment_parser],
        help='Note: This API is supported for Apigee Edge for Private Cloud only. For Apigee Edge for Public Cloud use Update an entry in an environment-scoped KVM. Updates an existing KeyValueMap in an environment. Does not override the existing map. Instead, this method updates the entries if they exist or adds them if not. It can take several minutes before the new value is visible to runtime traffic.')
    update_keyvaluemap_in_an_environment.add_argument('-n', '--name', help='name', required=True)
    update_keyvaluemap_in_an_environment.add_argument('-b', '--body', help='request body', required=True)
    update_keyvaluemap_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.update_keyvaluemap_in_an_environment(args).text))

    create_an_entry_in_an_environment_scoped_kvm = parser_keyvaluemaps.add_parser('create', aliases=['create-an-entry-in-an-environment-scoped-kvm'], parents=[parent_parser, environment_parser],
        help='Note: This API is supported for Apigee Edge for the Public Cloud only. Creates an entry in an existing KeyValueMap scoped to an environment. A key (name) cannot be larger than 2 KB. KVM names are case sensitive.')
    create_an_entry_in_an_environment_scoped_kvm.add_argument('-n', '--name', help='name', required=True)
    create_an_entry_in_an_environment_scoped_kvm.add_argument('--entry-name', help='entry name', required=True)
    create_an_entry_in_an_environment_scoped_kvm.add_argument('--entry-value', help='entry value', required=True)
    create_an_entry_in_an_environment_scoped_kvm.set_defaults(func=lambda args: print(keyvaluemaps.create_an_entry_in_an_environment_scoped_kvm(args).text))

    update_an_entry_in_an_environment_scoped_kvm = parser_keyvaluemaps.add_parser('update-entry', aliases=['update-an-entry-in-an-environment-scoped-kvm'], parents=[parent_parser, environment_parser],
        help='Note: This API is supported for Apigee Edge for the Public Cloud only. Updates an entry in a KeyValueMap scoped to an environment. A key cannot be larger than 2 KB. KVM names are case sensitive. Does not override the existing map. It can take several minutes before the new value is visible to runtime traffic.')
    update_an_entry_in_an_environment_scoped_kvm.add_argument('-n', '--name', help='name', required=True)
    update_an_entry_in_an_environment_scoped_kvm.add_argument('--entry-name', help='entry name', required=True)
    update_an_entry_in_an_environment_scoped_kvm.add_argument('--updated-value', help='updated value', required=True)
    update_an_entry_in_an_environment_scoped_kvm.set_defaults(func=lambda args: print(keyvaluemaps.update_an_entry_in_an_environment_scoped_kvm(args).text))

    list_keys_in_an_environment_scoped_keyvaluemap = parser_keyvaluemaps.add_parser('list-keys', aliases=['list-keys-in-an-environment-scoped-keyvaluemap'], parents=[parent_parser, environment_parser],
        help='Note: This API is supported for Apigee Edge for the Public Cloud only. Lists keys in a KeyValueMap scoped to an environment. KVM names are case sensitive.')
    list_keys_in_an_environment_scoped_keyvaluemap.add_argument('-n', '--name', help='name', required=True)
    list_keys_in_an_environment_scoped_keyvaluemap.add_argument('--startkey', default='',
        help='To filter the keys that are returned, enter the name of a key that the list will start with.')
    list_keys_in_an_environment_scoped_keyvaluemap.add_argument('--count', default=100,
        help='Limits the list of keys to the number you specify, up to a maximum of 100. Use with the startkey parameter to provide more targeted filtering.')
    list_keys_in_an_environment_scoped_keyvaluemap.set_defaults(func=lambda args: print(keyvaluemaps.list_keys_in_an_environment_scoped_keyvaluemap(args).text))

    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.error('too few arguments')
    func(args)

if __name__ == '__main__':
    main()
