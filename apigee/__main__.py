#!/usr/bin/env python
"""apigee"""

import argparse

import apigee

from apigee import APIGEE_CLI_PREFIX
from apigee.api import *
from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.file_parser import FileParser
from apigee.parsers.dir_parser import DirParser
from apigee.parsers.format_parser import FormatParser
# from apigee.parsers.environment_parser import EnvironmentParser
# from apigee.parsers.prefix_parser import PrefixParser
from apigee.util import *

@exception_handler
def main():
    parent_parser = ParentParser()
    prefix = authorization.get_credential(parent_parser.profile, 'prefix')

    # file_parser = argparse.ArgumentParser(add_help=False)
    # file_parser.add_argument('-f', '--file', action='store', help='file path', required=True, type=isfile)
    file_parser = FileParser()

    # dir_parser = argparse.ArgumentParser(add_help=False)
    # dir_parser.add_argument('-d', '--directory', action='store', help='directory path', required=True, type=isdir)
    dir_parser = DirParser()

    # format_parser = argparse.ArgumentParser(add_help=False)
    # format_parser.add_argument('-F', '--format', action='store', help='output format type', required=False)
    format_parser = FormatParser()

    environment_parser = argparse.ArgumentParser(add_help=False)
    environment_parser.add_argument('-e', '--environment', help='environment', required=True)

    prefix_parser = argparse.ArgumentParser(add_help=False)
    prefix_parser.add_argument('--prefix', help='prefix filter for apigee items', default=APIGEE_CLI_PREFIX if prefix is None else prefix)

    parser = argparse.ArgumentParser(prog=apigee.CMD, description=apigee.description)
    parser.add_argument('-V', '--version', action='version', version=apigee.APP + ' ' + apigee.__version__)
    subparsers = parser.add_subparsers()

    parser_test = subparsers.add_parser('test', aliases=['get-access-token'], help='test get access token', parents=[parent_parser()])
    parser_test.set_defaults(func=test)

    parser_configure = subparsers.add_parser('configure', help='configure credentials')
    parser_configure.add_argument('-P', '--profile', help='name of profile to create', default='default')
    parser_configure.set_defaults(func=config.main)

    parser_apis = subparsers.add_parser('apis', help='apis').add_subparsers()
    parser_deployments = subparsers.add_parser('deployments', aliases=['deps'], help='see apis that are actively deployed').add_subparsers()
    parser_keyvaluemaps = subparsers.add_parser('kvms', aliases=['keyvaluemaps'], help='keyvaluemaps').add_subparsers()
    parser_developers = subparsers.add_parser('developers', aliases=['devs'], help='developers').add_subparsers()
    parser_apps = subparsers.add_parser('apps', help='developer apps').add_subparsers()
    parser_apiproducts = subparsers.add_parser('products', aliases=['prods'], help='api products').add_subparsers()
    parser_targetservers = subparsers.add_parser('ts', aliases=['targetservers'], help='target servers').add_subparsers()
    parser_maskconfigs = subparsers.add_parser('mask', aliases=['maskconfigs'], help='data masks').add_subparsers()
    parser_permissions = subparsers.add_parser('perms', aliases=['permissions'], help='manage permissions for a role').add_subparsers()

    parser_prepend = subparsers.add_parser('prepend', aliases=['prefix'], help='prepend all matching strings with a prefix in all files in the specified directory (rudimentary stream editor). this is potentially VERY DANGEROUS. make sure you have version control such as Git to revert any changes in the target directory.', parents=[dir_parser()])
    parser_prepend.add_argument('-P', '--prefix', help='prefix to prepend', required=True)
    parser_prepend.add_argument('-r', '--resource', help='apigee resource to be prepended', required=True)
    parser_prepend.set_defaults(func=prepend.main)

    apis_deploy = parser_apis.add_parser('deploy', help='deploy apis', parents=[parent_parser(), dir_parser(), environment_parser])
    apis_deploy.add_argument('-n', '--name', help='name', required=True)
    # apis_deploy.add_argument('-d', '--directory', help='directory name')
    # apis_deploy.add_argument('-p', '--path', help='base path')
    apis_deploy.add_argument('-i', '--import-only', action='store_true', help='denotes to import only and not actually deploy')
    apis_deploy.add_argument('-s', '--seamless-deploy', action='store_true', help='seamless deploy the bundle')
    apis_deploy.set_defaults(func=deploy.deploy)

    export_api_proxy = parser_apis.add_parser('export', aliases=['export-api-proxy'], parents=[parent_parser()],
        help='Outputs an API proxy revision as a ZIP formatted bundle of code and config files. This enables local configuration and development, including attachment of policies and scripts.')
    export_api_proxy.add_argument('-n', '--name', help='name', required=True)
    export_api_proxy.add_argument('-r', '--revision-number', help='revision number', required=True)
    export_api_proxy.add_argument('-O', '--output-file', help='output file')
    # export_api_proxy.set_defaults(func=lambda args: print(apis.export_api_proxy(args).text))
    export_api_proxy.set_defaults(func=apis.export_api_proxy)

    get_api_proxy = parser_apis.add_parser('get', aliases=['get-api-proxy'], parents=[parent_parser()],
        help='Gets an API proxy by name, including a list of existing revisions of the proxy.')
    get_api_proxy.add_argument('-n', '--name', help='name', required=True)
    get_api_proxy.set_defaults(func=lambda args: print(apis.get_api_proxy(args).text))

    list_api_proxies = parser_apis.add_parser('list', aliases=['list-api-proxies'], parents=[parent_parser(), prefix_parser],
        help='Gets the names of all API proxies in an organization. The names correspond to the names defined in the configuration files for each API proxy.')
    list_api_proxies.set_defaults(func=lambda args: print(apis.list_api_proxies(args)))

    get_api_proxy_deployment_details = parser_deployments.add_parser('get', aliases=['get-api-proxy-deployment-details'], parents=[parent_parser()],
        help='Returns detail on all deployments of the API proxy for all environments. All deployments are listed in the test and prod environments, as well as other environments, if they exist.')
    get_api_proxy_deployment_details.add_argument('-n', '--name', help='name', required=True)
    get_api_proxy_deployment_details.add_argument('-r', '--revision-name', action='store_true', help='get revisions only')
    get_api_proxy_deployment_details.add_argument('-j', '--json', action='store_true', help='use json output')
    get_api_proxy_deployment_details.add_argument('--max-colwidth', help='max column width', type=int, default=40)
    get_api_proxy_deployment_details.set_defaults(func=lambda args: print(deployments.get_api_proxy_deployment_details(args)))

    create_keyvaluemap_in_an_environment = parser_keyvaluemaps.add_parser('create', aliases=['create-keyvaluemap-in-an-environment'], parents=[parent_parser(), environment_parser],
        help='Creates a key value map in an environment.')
    create_keyvaluemap_in_an_environment.add_argument('-b', '--body', help='request body', required=True)
    create_keyvaluemap_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.create_keyvaluemap_in_an_environment(args).text))

    delete_keyvaluemap_from_an_environment = parser_keyvaluemaps.add_parser('delete', aliases=['delete-keyvaluemap-from-an-environment'], parents=[parent_parser(), environment_parser],
        help='Deletes a key/value map and all associated entries from an environment.')
    delete_keyvaluemap_from_an_environment.add_argument('-n', '--name', help='name', required=True)
    delete_keyvaluemap_from_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.delete_keyvaluemap_from_an_environment(args).text))

    delete_keyvaluemap_entry_in_an_environment = parser_keyvaluemaps.add_parser('delete-entry', aliases=['delete-keyvaluemap-entry-in-an-environment'], parents=[parent_parser(), environment_parser],
        help='Deletes a specific key/value map entry in an environment by name, along with associated entries.')
    delete_keyvaluemap_entry_in_an_environment.add_argument('-n', '--name', help='name', required=True)
    delete_keyvaluemap_entry_in_an_environment.add_argument('--entry-name', help='entry name', required=True)
    delete_keyvaluemap_entry_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.delete_keyvaluemap_entry_in_an_environment(args).text))

    get_keyvaluemap_in_an_environment = parser_keyvaluemaps.add_parser('get', aliases=['get-keyvaluemap-in-an-environment'], parents=[parent_parser(), environment_parser],
        help='Gets a KeyValueMap (KVM) in an environment by name, along with the keys and values.')
    get_keyvaluemap_in_an_environment.add_argument('-n', '--name', help='name', required=True)
    get_keyvaluemap_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.get_keyvaluemap_in_an_environment(args).text))

    get_a_keys_value_in_an_environment_scoped_keyvaluemap = parser_keyvaluemaps.add_parser('get-value', aliases=['get-a-keys-value-in-an-environment-scoped-keyvaluemap'], parents=[parent_parser(), environment_parser],
        help='Gets the value of a key in an environment-scoped KeyValueMap (KVM).')
    get_a_keys_value_in_an_environment_scoped_keyvaluemap.add_argument('-n', '--name', help='name', required=True)
    get_a_keys_value_in_an_environment_scoped_keyvaluemap.add_argument('--entry-name', help='entry name', required=True)
    get_a_keys_value_in_an_environment_scoped_keyvaluemap.set_defaults(func=lambda args: print(keyvaluemaps.get_a_keys_value_in_an_environment_scoped_keyvaluemap(args).text))

    list_keyvaluemaps_in_an_environment = parser_keyvaluemaps.add_parser('list', aliases=['list-keyvaluemaps-in-an-environment'], parents=[parent_parser(), environment_parser, prefix_parser],
        help='Lists the name of all key/value maps in an environment and optionally returns an expanded view of all key/value maps for the environment.')
    list_keyvaluemaps_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.list_keyvaluemaps_in_an_environment(args)))

    update_keyvaluemap_in_an_environment = parser_keyvaluemaps.add_parser('update', aliases=['update-keyvaluemap-in-an-environment'], parents=[parent_parser(), environment_parser],
        help='Note: This API is supported for Apigee Edge for Private Cloud only. For Apigee Edge for Public Cloud use Update an entry in an environment-scoped KVM. Updates an existing KeyValueMap in an environment. Does not override the existing map. Instead, this method updates the entries if they exist or adds them if not. It can take several minutes before the new value is visible to runtime traffic.')
    update_keyvaluemap_in_an_environment.add_argument('-n', '--name', help='name', required=True)
    update_keyvaluemap_in_an_environment.add_argument('-b', '--body', help='request body', required=True)
    update_keyvaluemap_in_an_environment.set_defaults(func=lambda args: print(keyvaluemaps.update_keyvaluemap_in_an_environment(args).text))

    create_an_entry_in_an_environment_scoped_kvm = parser_keyvaluemaps.add_parser('create-entry', aliases=['create-an-entry-in-an-environment-scoped-kvm'], parents=[parent_parser(), environment_parser],
        help='Note: This API is supported for Apigee Edge for the Public Cloud only. Creates an entry in an existing KeyValueMap scoped to an environment. A key (name) cannot be larger than 2 KB. KVM names are case sensitive.')
    create_an_entry_in_an_environment_scoped_kvm.add_argument('-n', '--name', help='name', required=True)
    create_an_entry_in_an_environment_scoped_kvm.add_argument('--entry-name', help='entry name', required=True)
    create_an_entry_in_an_environment_scoped_kvm.add_argument('--entry-value', help='entry value', required=True)
    create_an_entry_in_an_environment_scoped_kvm.set_defaults(func=lambda args: print(keyvaluemaps.create_an_entry_in_an_environment_scoped_kvm(args).text))

    update_an_entry_in_an_environment_scoped_kvm = parser_keyvaluemaps.add_parser('update-entry', aliases=['update-an-entry-in-an-environment-scoped-kvm'], parents=[parent_parser(), environment_parser],
        help='Note: This API is supported for Apigee Edge for the Public Cloud only. Updates an entry in a KeyValueMap scoped to an environment. A key cannot be larger than 2 KB. KVM names are case sensitive. Does not override the existing map. It can take several minutes before the new value is visible to runtime traffic.')
    update_an_entry_in_an_environment_scoped_kvm.add_argument('-n', '--name', help='name', required=True)
    update_an_entry_in_an_environment_scoped_kvm.add_argument('--entry-name', help='entry name', required=True)
    update_an_entry_in_an_environment_scoped_kvm.add_argument('--updated-value', help='updated value', required=True)
    update_an_entry_in_an_environment_scoped_kvm.set_defaults(func=lambda args: print(keyvaluemaps.update_an_entry_in_an_environment_scoped_kvm(args).text))

    list_keys_in_an_environment_scoped_keyvaluemap = parser_keyvaluemaps.add_parser('list-keys', aliases=['list-keys-in-an-environment-scoped-keyvaluemap'], parents=[parent_parser(), environment_parser, prefix_parser],
        help='Note: This API is supported for Apigee Edge for the Public Cloud only. Lists keys in a KeyValueMap scoped to an environment. KVM names are case sensitive.')
    list_keys_in_an_environment_scoped_keyvaluemap.add_argument('-n', '--name', help='name', required=True)
    list_keys_in_an_environment_scoped_keyvaluemap.add_argument('--startkey', default='',
        help='To filter the keys that are returned, enter the name of a key that the list will start with.')
    list_keys_in_an_environment_scoped_keyvaluemap.add_argument('--count', default=100, type=int,
        help='Limits the list of keys to the number you specify, up to a maximum of 100. Use with the startkey parameter to provide more targeted filtering.')
    list_keys_in_an_environment_scoped_keyvaluemap.set_defaults(func=lambda args: print(keyvaluemaps.list_keys_in_an_environment_scoped_keyvaluemap(args)))

    push_keyvaluemap = parser_keyvaluemaps.add_parser('push', aliases=['push-keyvaluemap'], parents=[parent_parser(), environment_parser, file_parser()],
        help='Push KeyValueMap to Apigee. This will create KeyValueMap/entries if they do not exist, update existing KeyValueMap/entries, and delete entries on Apigee that are not present in the request body.')
    # push_keyvaluemap.add_argument('-n', '--name', help='name', required=True)
    push_keyvaluemap.set_defaults(func=lambda args: keyvaluemaps.push_keyvaluemap(args))

    list_developers = parser_developers.add_parser('list', aliases=['list-developers'], parents=[parent_parser(), prefix_parser],
        help='Lists all developers in an organization by email address. This call does not list any company developers who are a part of the designated organization.')
    list_developers.add_argument('--expand', action='store_true',
        help='Set to true to list developers exanded with details.')
    list_developers.add_argument('--count', default=1000, type=int,
        help='Limits the list to the number you specify. Use with the startKey parameter to provide more targeted filtering. The limit is 1000.')
    list_developers.add_argument('--startkey', default='',
        help='To filter the keys that are returned, enter the email of a developer that the list will start with.')
    list_developers.set_defaults(func=lambda args: print(developers.list_developers(args)))

    create_developer_app = parser_apps.add_parser('create', aliases=['create-developer-app'], parents=[parent_parser()],
        help='Creates an app associated with a developer, associates the app with an API product, and auto-generates an API key for the app to use in calls to API proxies inside the API product.')
    create_developer_app.add_argument('-d', '--developer', help='developer email or id', required=True)
    create_developer_app.add_argument('-b', '--body', help='request body', required=True)
    create_developer_app.set_defaults(func=lambda args: print(apps.create_developer_app(args).text))

    create_empty_developer_app = parser_apps.add_parser('create-empty', aliases=['create-empty-developer-app'], parents=[parent_parser()],
        help='Creates an empty developer app.')
    create_empty_developer_app.add_argument('-d', '--developer', help='developer email or id', required=True)
    create_empty_developer_app.add_argument('-n', '--name', help='Name of the app. The name is the unique ID of the app for this organization and developer.', required=True)
    # create_empty_developer_app.add_argument('--products', help='A list of API products associated with the app\'s credentials', nargs='+', required=False, default=[])
    create_empty_developer_app.add_argument('--display-name', help='The DisplayName (set with an attribute) is what appears in the management UI. If you don\'t provide a DisplayName, the name is used.', required=False, default=None)
    # create_empty_developer_app.add_argument('--scopes', help='Sets the scopes element under the apiProducts element in the attributes of the app. The specified scopes must already exist on the API products associated with the app.', nargs='+', required=False, default=[])
    create_empty_developer_app.add_argument('--callback-url', help='The callbackUrl is used by OAuth 2.0 authorization servers to communicate authorization codes back to apps. CallbackUrl must match the value of redirect_uri in some OAuth 2.0 See the documentation on OAuth 2.0 for more details.', required=False, default=None)
    create_empty_developer_app.set_defaults(func=lambda args: print(apps.create_empty_developer_app(args).text))

    create_a_consumer_key_and_secret = parser_apps.add_parser('create-creds', aliases=['create-a-consumer-key-and-secret', 'create-credentials'], parents=[parent_parser()],
        help='Creates a custom consumer key and secret for a developer app. This is particularly useful if you want to migrate existing consumer keys/secrets to Edge from another system. Consumer keys and secrets can contain letters, numbers, underscores, and hyphens. No other special characters are allowed.')
    create_a_consumer_key_and_secret.add_argument('-d', '--developer', help='developer email or id', required=True)
    create_a_consumer_key_and_secret.add_argument('-n', '--name', help='Name of the app. The name is the unique ID of the app for this organization and developer.', required=True)
    create_a_consumer_key_and_secret.add_argument('--consumer-key', help='', required=False, default=None)
    create_a_consumer_key_and_secret.add_argument('--consumer-secret', help='', required=False, default=None)
    create_a_consumer_key_and_secret.add_argument('--key-length', help='length of consumer key', required=False, default=32)
    create_a_consumer_key_and_secret.add_argument('--secret-length', help='length of consumer secret', required=False, default=32)
    create_a_consumer_key_and_secret.add_argument('--key-suffix', help='', required=False, default=None)
    create_a_consumer_key_and_secret.add_argument('--key-delimiter', help="separates consumerKey and key suffix with a delimiter. the default is '-'.", required=False, default='-')
    create_a_consumer_key_and_secret.add_argument('--products', help='A list of API products to be associated with the app\'s credentials', nargs='+', required=False, default=[])
    create_a_consumer_key_and_secret.set_defaults(func=lambda args: print(apps.create_a_consumer_key_and_secret(args).text))

    list_developer_apps = parser_apps.add_parser('list', aliases=['list-developer-apps'], parents=[parent_parser(), prefix_parser],
        help='Lists all apps created by a developer in an organization, and optionally provides an expanded view of the apps. All time values in the response are UNIX times. You can specify either the developer\'s email address or Edge ID.')
    list_developer_apps.add_argument('-d', '--developer', help='developer email or id', required=True)
    list_developer_apps.add_argument('--expand', action='store_true',
        help='Set to true to expand the results. This query parameter does not work if you use the count or startKey query parameters.')
    list_developer_apps.add_argument('--count', default=100, type=int,
        help='Limits the list to the number you specify. The limit is 100. Use with the startKey parameter to provide more targeted filtering.')
    list_developer_apps.add_argument('--startkey', default='',
        help='To filter the keys that are returned, enter the name of a company app that the list will start with.')
    list_developer_apps.set_defaults(func=lambda args: print(apps.list_developer_apps(args)))

    get_developer_app_details = parser_apps.add_parser('get', aliases=['get-developer-app-details'], parents=[parent_parser()],
        help='Get the profile of a specific developer app. All times in the response are UNIX times. Note that the response contains a top-level attribute named accessType that is no longer used by Apigee.')
    get_developer_app_details.add_argument('-d', '--developer', help='developer email or id', required=True)
    get_developer_app_details.add_argument('-n', '--name', help='name', required=True)
    get_developer_app_details.set_defaults(func=lambda args: print(apps.get_developer_app_details(args).text))

    list_api_products = parser_apiproducts.add_parser('list', aliases=['list-api-products'], parents=[parent_parser(), prefix_parser],
        help='Get a list of all API product names for an organization.')
    list_api_products.add_argument('--expand', action='store_true',
        help='Set to \'true\' to get expanded details about each product.')
    list_api_products.add_argument('--count', default=1000, type=int,
        help='Number of API products to return in the API call. The maximum limit is 1000. Use with the startkey to provide more targeted filtering.')
    list_api_products.add_argument('--startkey', default='',
        help='Returns a list of API products starting with the specified API product.')
    list_api_products.set_defaults(func=lambda args: print(apiproducts.list_api_products(args)))

    get_api_product = parser_apiproducts.add_parser('get', aliases=['get-api-product'], parents=[parent_parser()],
        help='Gets configuration data for an API product. The API product name required in the request URL is not the "Display Name" value displayed for the API product in the Edge UI. While they may be the same, they are not always the same depending on whether the API product was created via UI or API.')
    get_api_product.add_argument('-n', '--name', help='name', required=True)
    get_api_product.set_defaults(func=lambda args: print(apiproducts.get_api_product(args).text))

    create_a_targetserver = parser_targetservers.add_parser('create', aliases=['create-a-targetserver'], parents=[parent_parser(), environment_parser],
        help='Create a TargetServer in the specified environment. TargetServers are used to decouple TargetEndpoint HTTPTargetConnections from concrete URLs for backend services.')
    create_a_targetserver.add_argument('-b', '--body', help='request body', required=True)
    create_a_targetserver.set_defaults(func=lambda args: print(targetservers.create_a_targetserver(args).text))

    delete_a_targetserver = parser_targetservers.add_parser('delete', aliases=['delete-a-targetserver'], parents=[parent_parser(), environment_parser],
        help='Delete a TargetServer configuration from an environment. Returns information about the deleted TargetServer.')
    delete_a_targetserver.add_argument('-n', '--name', help='name', required=True)
    delete_a_targetserver.set_defaults(func=lambda args: print(targetservers.delete_a_targetserver(args).text))

    list_targetservers_in_an_environment = parser_targetservers.add_parser('list', aliases=['list-targetservers-in-an-environment'], parents=[parent_parser(), environment_parser, prefix_parser],
        help='List all TargetServers in an environment.')
    list_targetservers_in_an_environment.set_defaults(func=lambda args: print(targetservers.list_targetservers_in_an_environment(args)))

    get_targetserver = parser_targetservers.add_parser('get', aliases=['get-targetserver'], parents=[parent_parser(), environment_parser],
        help='Returns a TargetServer definition.')
    get_targetserver.add_argument('-n', '--name', help='name', required=True)
    get_targetserver.set_defaults(func=lambda args: print(targetservers.get_targetserver(args).text))

    update_a_targetserver = parser_targetservers.add_parser('update', aliases=['update-a-targetserver'], parents=[parent_parser(), environment_parser],
        help='Modifies an existing TargetServer.')
    update_a_targetserver.add_argument('-n', '--name', help='name', required=True)
    update_a_targetserver.add_argument('-b', '--body', help='request body', required=True)
    update_a_targetserver.set_defaults(func=lambda args: print(targetservers.update_a_targetserver(args).text))

    push_targetserver = parser_targetservers.add_parser('push', aliases=['push-targetserver'], parents=[parent_parser(), environment_parser, file_parser()],
        help='Push TargetServer to Apigee. This will create/update a TargetServer.')
    # push_keyvaluemap.add_argument('-n', '--name', help='name', required=True)
    push_targetserver.set_defaults(func=lambda args: targetservers.push_targetserver(args))

    create_data_masks_for_an_api_proxy = parser_maskconfigs.add_parser('create-api', aliases=['create-data-masks-for-an-api-proxy'], parents=[parent_parser()],
        help='Create a data mask for an API proxy. You can capture message content to assist in runtime debugging of APIs calls. In many cases, API traffic contains sensitive data, such credit cards or personally identifiable health information (PHI) that needs to filtered out of the captured message content. Data masks enable you to specify data that will be filtered out of trace sessions. Data masking is only enabled when a trace session (also called a \'debug\' session) is enabled for an API proxy. If no trace session are enabled on an API proxy, then the data will not be masked.')
    create_data_masks_for_an_api_proxy.add_argument('-n', '--name', help='name', required=True)
    create_data_masks_for_an_api_proxy.add_argument('-b', '--body', help='request body', required=True)
    create_data_masks_for_an_api_proxy.set_defaults(func=lambda args: print(maskconfigs.create_data_masks_for_an_api_proxy(args).text))

    delete_data_masks_for_an_api_proxy = parser_maskconfigs.add_parser('delete-api', aliases=['delete-data-masks-for-an-api-proxy'], parents=[parent_parser()],
        help='Delete a data mask for an API proxy.')
    delete_data_masks_for_an_api_proxy.add_argument('-n', '--name', help='name', required=True)
    delete_data_masks_for_an_api_proxy.add_argument('--maskconfig-name', help='data mask name', required=True)
    delete_data_masks_for_an_api_proxy.set_defaults(func=lambda args: print(maskconfigs.delete_data_masks_for_an_api_proxy(args).text))

    get_data_mask_details_for_an_api_proxy = parser_maskconfigs.add_parser('get-api', aliases=['get-data-mask-details-for-an-api-proxy'], parents=[parent_parser()],
        help='Get the details for a data mask for an API proxy.')
    get_data_mask_details_for_an_api_proxy.add_argument('-n', '--name', help='name', required=True)
    get_data_mask_details_for_an_api_proxy.add_argument('--maskconfig-name', help='data mask name', required=True)
    get_data_mask_details_for_an_api_proxy.set_defaults(func=lambda args: print(maskconfigs.get_data_mask_details_for_an_api_proxy(args).text))

    list_data_masks_for_an_api_proxy = parser_maskconfigs.add_parser('list-api', aliases=['list-data-masks-for-an-api-proxy'], parents=[parent_parser()],
        help='List all data masks for an API proxy.')
    list_data_masks_for_an_api_proxy.add_argument('-n', '--name', help='name', required=True)
    list_data_masks_for_an_api_proxy.set_defaults(func=lambda args: print(maskconfigs.list_data_masks_for_an_api_proxy(args).text))

    list_data_masks_for_an_organization = parser_maskconfigs.add_parser('list', aliases=['list-data-masks-for-an-organization'], parents=[parent_parser()],
        help='List all data masks for an organization.')
    list_data_masks_for_an_organization.set_defaults(func=lambda args: print(maskconfigs.list_data_masks_for_an_organization(args).text))

    create_permissions = parser_permissions.add_parser('create', aliases=['create-permissions'], parents=[parent_parser()],
        help='Create permissions for a role.')
    create_permissions.add_argument('-n', '--name', help='name', required=True)
    create_permissions.add_argument('-b', '--body', help='request body', required=True)
    create_permissions.set_defaults(func=lambda args: print(permissions.create_permissions(args).text))

    team_permissions = parser_permissions.add_parser('team', aliases=['team-permissions'], parents=[parent_parser()],
        help='Create default permissions for a team role based on a template.')
    team_permissions.add_argument('-n', '--name', help='name of user role', required=True)
    team_permissions.add_argument('-t', '--team', help='team prefix/code', required=True)
    team_permissions.set_defaults(func=lambda args: print(permissions.team_permissions(args).text))

    get_permissions = parser_permissions.add_parser('get', aliases=['get-permissions'], parents=[parent_parser()],
        help='Get permissions for a role.')
    get_permissions.add_argument('-n', '--name', help='name', required=True)
    get_permissions.add_argument('-j', '--json', action='store_true', help='use json output')
    get_permissions.add_argument('--max-colwidth', help='max column width', type=int, default=40)
    get_permissions.set_defaults(func=lambda args: print(permissions.get_permissions(args)))

    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.error('too few arguments')
    func(args)

if __name__ == '__main__':
    main()
