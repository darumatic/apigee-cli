#!/usr/bin/env python
"""apigee"""

import argparse
import os
import sys

import apigee

from apigee import APIGEE_CLI_PREFIX
from apigee import APIGEE_ORG
from apigee import APIGEE_USERNAME
from apigee import APIGEE_PASSWORD
from apigee import APIGEE_MFA_SECRET
from apigee.api import *
from apigee.util import *

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

    prefix_parser = argparse.ArgumentParser(add_help=False)
    prefix_parser.add_argument('--prefix', help='prefix filter for apigee items', default=APIGEE_CLI_PREFIX)

    parser = argparse.ArgumentParser(prog=apigee.CMD, description=apigee.description)
    parser.add_argument('-V', '--version', action='version', version=apigee.APP + ' ' + apigee.__version__)
    subparsers = parser.add_subparsers()

    parser_test = subparsers.add_parser('test', help='test get access token', parents=[parent_parser])
    parser_test.set_defaults(func=test)

    parser_apis = subparsers.add_parser('apis', help='apis').add_subparsers()
    parser_deployments = subparsers.add_parser('deployments', aliases=['deps'], help='see apis that are actively deployed').add_subparsers()
    parser_keyvaluemaps = subparsers.add_parser('kvms', aliases=['keyvaluemaps'], help='keyvaluemaps').add_subparsers()
    parser_developers = subparsers.add_parser('developers', aliases=['devs'], help='developers').add_subparsers()
    parser_apps = subparsers.add_parser('apps', help='developer apps').add_subparsers()
    parser_apiproducts = subparsers.add_parser('products', aliases=['prods'], help='api products').add_subparsers()
    parser_targetservers = subparsers.add_parser('ts', aliases=['targetservers'], help='target servers').add_subparsers()

    parser_prepend = subparsers.add_parser('prepend', aliases=['prefix'], help='prepend all matching strings with a prefix in all files in the specified directory (rudimentary stream editor). this is potentially VERY DANGEROUS. make sure you have version control such as Git to revert any changes in the target directory.', parents=[dir_parser])
    parser_prepend.add_argument('-P', '--prefix', help='prefix to prepend', required=True)
    parser_prepend.add_argument('-r', '--resource', help='apigee resource to be prepended', required=True)
    parser_prepend.set_defaults(func=prepend.main)

    apis_deploy = parser_apis.add_parser('deploy', help='deploy apis', parents=[parent_parser, dir_parser, environment_parser])
    apis_deploy.add_argument('-n', '--name', help='name', required=True)
    # apis_deploy.add_argument('-d', '--directory', help='directory name')
    # apis_deploy.add_argument('-p', '--path', help='base path')
    apis_deploy.add_argument('-i', '--import-only', action='store_true', help='denotes to import only and not actually deploy')
    apis_deploy.add_argument('-s', '--seamless-deploy', action='store_true', help='seamless deploy the bundle')
    apis_deploy.set_defaults(func=deploy.deploy)

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

    list_api_proxies = parser_apis.add_parser('list', aliases=['list-api-proxies'], parents=[parent_parser, prefix_parser],
        help='Gets the names of all API proxies in an organization. The names correspond to the names defined in the configuration files for each API proxy.')
    list_api_proxies.set_defaults(func=lambda args: print(apis.list_api_proxies(args)))

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

    list_keyvaluemaps_in_an_environment = parser_keyvaluemaps.add_parser('list', aliases=['list-keyvaluemaps-in-an-environment'], parents=[parent_parser, environment_parser, prefix_parser],
        help='Lists the name of all key/value maps in an environment and optionally returns an expanded view of all key/value maps for the environment.')
    list_keyvaluemaps_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.list_keyvaluemaps_in_an_environment(args)))

    update_keyvaluemap_in_an_environment = parser_keyvaluemaps.add_parser('update', aliases=['update-keyvaluemap-in-an-environment'], parents=[parent_parser, environment_parser],
        help='Note: This API is supported for Apigee Edge for Private Cloud only. For Apigee Edge for Public Cloud use Update an entry in an environment-scoped KVM. Updates an existing KeyValueMap in an environment. Does not override the existing map. Instead, this method updates the entries if they exist or adds them if not. It can take several minutes before the new value is visible to runtime traffic.')
    update_keyvaluemap_in_an_environment.add_argument('-n', '--name', help='name', required=True)
    update_keyvaluemap_in_an_environment.add_argument('-b', '--body', help='request body', required=True)
    update_keyvaluemap_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.update_keyvaluemap_in_an_environment(args).text))

    create_an_entry_in_an_environment_scoped_kvm = parser_keyvaluemaps.add_parser('create-entry', aliases=['create-an-entry-in-an-environment-scoped-kvm'], parents=[parent_parser, environment_parser],
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

    list_keys_in_an_environment_scoped_keyvaluemap = parser_keyvaluemaps.add_parser('list-keys', aliases=['list-keys-in-an-environment-scoped-keyvaluemap'], parents=[parent_parser, environment_parser, prefix_parser],
        help='Note: This API is supported for Apigee Edge for the Public Cloud only. Lists keys in a KeyValueMap scoped to an environment. KVM names are case sensitive.')
    list_keys_in_an_environment_scoped_keyvaluemap.add_argument('-n', '--name', help='name', required=True)
    list_keys_in_an_environment_scoped_keyvaluemap.add_argument('--startkey', default='',
        help='To filter the keys that are returned, enter the name of a key that the list will start with.')
    list_keys_in_an_environment_scoped_keyvaluemap.add_argument('--count', default=100, type=int,
        help='Limits the list of keys to the number you specify, up to a maximum of 100. Use with the startkey parameter to provide more targeted filtering.')
    list_keys_in_an_environment_scoped_keyvaluemap.set_defaults(func=lambda args: print(keyvaluemaps.list_keys_in_an_environment_scoped_keyvaluemap(args)))

    list_developers = parser_developers.add_parser('list', aliases=['list-developers'], parents=[parent_parser, prefix_parser],
        help='Lists all developers in an organization by email address. This call does not list any company developers who are a part of the designated organization.')
    list_developers.add_argument('--expand', action='store_true',
        help='Set to true to list developers exanded with details.')
    list_developers.add_argument('--count', default=1000, type=int,
        help='Limits the list to the number you specify. Use with the startKey parameter to provide more targeted filtering. The limit is 1000.')
    list_developers.add_argument('--startkey', default='',
        help='To filter the keys that are returned, enter the email of a developer that the list will start with.')
    list_developers.set_defaults(func=lambda args: print(developers.list_developers(args)))

    list_developer_apps = parser_apps.add_parser('list', aliases=['list-developer-apps'], parents=[parent_parser, prefix_parser],
        help='Lists all apps created by a developer in an organization, and optionally provides an expanded view of the apps. All time values in the response are UNIX times. You can specify either the developer\'s email address or Edge ID.')
    list_developer_apps.add_argument('-d', '--developer', help='developer email or id', required=True)
    list_developer_apps.add_argument('--expand', action='store_true',
        help='Set to true to expand the results. This query parameter does not work if you use the count or startKey query parameters.')
    list_developer_apps.add_argument('--count', default=100, type=int,
        help='Limits the list to the number you specify. The limit is 100. Use with the startKey parameter to provide more targeted filtering.')
    list_developer_apps.add_argument('--startkey', default='',
        help='To filter the keys that are returned, enter the name of a company app that the list will start with.')
    list_developer_apps.set_defaults(func=lambda args: print(apps.list_developer_apps(args)))

    get_developer_app_details = parser_apps.add_parser('get', aliases=['get-developer-app-details'], parents=[parent_parser],
        help='Get the profile of a specific developer app. All times in the response are UNIX times. Note that the response contains a top-level attribute named accessType that is no longer used by Apigee.')
    get_developer_app_details.add_argument('-d', '--developer', help='developer email or id', required=True)
    get_developer_app_details.add_argument('-n', '--name', help='name', required=True)
    get_developer_app_details.set_defaults(func=lambda args: print(apps.get_developer_app_details(args).text))

    list_api_products = parser_apiproducts.add_parser('list', aliases=['list-api-products'], parents=[parent_parser, prefix_parser],
        help='Get a list of all API product names for an organization.')
    list_api_products.add_argument('--expand', action='store_true',
        help='Set to \'true\' to get expanded details about each product.')
    list_api_products.add_argument('--count', default=1000, type=int,
        help='Number of API products to return in the API call. The maximum limit is 1000. Use with the startkey to provide more targeted filtering.')
    list_api_products.add_argument('--startkey', default='',
        help='Returns a list of API products starting with the specified API product.')
    list_api_products.set_defaults(func=lambda args: print(apiproducts.list_api_products(args)))

    get_api_product = parser_apiproducts.add_parser('get', aliases=['get-api-product'], parents=[parent_parser],
        help='Gets configuration data for an API product. The API product name required in the request URL is not the "Display Name" value displayed for the API product in the Edge UI. While they may be the same, they are not always the same depending on whether the API product was created via UI or API.')
    get_api_product.add_argument('-n', '--name', help='name', required=True)
    get_api_product.set_defaults(func=lambda args: print(apiproducts.get_api_product(args).text))

    list_targetservers_in_an_environment = parser_targetservers.add_parser('list', aliases=['list-targetservers-in-an-environment'], parents=[parent_parser, environment_parser, prefix_parser],
        help='List all TargetServers in an environment.')
    list_targetservers_in_an_environment.set_defaults(func=lambda args: print(targetservers.list_targetservers_in_an_environment(args)))

    get_targetserver = parser_targetservers.add_parser('get', aliases=['get-targetserver'], parents=[parent_parser, environment_parser],
        help='Returns a TargetServer definition.')
    get_targetserver.add_argument('-n', '--name', help='name', required=True)
    get_targetserver.set_defaults(func=lambda args: print(targetservers.get_targetserver(args).text))

    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.error('too few arguments')
    func(args)

if __name__ == '__main__':
    main()
