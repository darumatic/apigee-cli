import json
import os
from typing import Any, List, Optional, Set
from dataclasses import dataclass
from pathlib import Path

from requests.exceptions import HTTPError
from tqdm import tqdm

from apigee import console
from apigee.apiproducts.apiproducts import Apiproducts
from apigee.apis.apis import Apis
from apigee.apps.apps import Apps
from apigee.caches.caches import Caches
from apigee.developers.developers import Developers
from apigee.exceptions import log_and_echo_http_error
from apigee.keyvaluemaps.keyvaluemaps import Keyvaluemaps
from apigee.permissions.permissions import Permissions
from apigee.targetservers.targetservers import Targetservers
from apigee.types import APIGEE_API_CHOICES, empty_snapshot, Struct
from apigee.userroles.userroles import Userroles
from apigee.utils import (extract_zip_file, filter_out_empty_values, get_resolved_directory_path, write_content_to_file)

APIS_SNAPSHOT_TARGET_SUBPATH = "snapshots/apis/{api}.json"
# APIS_TARGET_SUBPATH = 'apis/{api}/revision/{api}.zip'
KEYVALUEMAPS_SNAPSHOT_TARGET_SUBPATH = "snapshots/keyvaluemaps/{environment}/keyvaluemaps.json"
KEYVALUEMAPS_TARGET_SUBPATH = "keyvaluemaps/{environment}/{kvm}.json"
TARGETSERVERS_SNAPSHOT_TARGET_SUBPATH = "snapshots/targetservers/{environment}/targetservers.json"
TARGETSERVERS_TARGET_SUBPATH = "targetservers/{environment}/{targetserver}.json"
CACHES_SNAPSHOT_TARGET_SUBPATH = "snapshots/caches/{environment}/caches.json"
CACHES_TARGET_SUBPATH = "caches/{environment}/{cache}.json"
DEVELOPERS_SNAPSHOT_TARGET_SUBPATH = "snapshots/developers/developers.json"
DEVELOPERS_TARGET_SUBPATH = "developers/{developer}.json"
APIPRODUCTS_SNAPSHOT_TARGET_SUBPATH = "snapshots/apiproducts/apiproducts.json"
APIPRODUCTS_TARGET_SUBPATH = "apiproducts/{apiproduct}.json"
APPS_SNAPSHOT_TARGET_SUBPATH = "snapshots/apps/{app}.json"
APPS_TARGET_SUBPATH = "apps/{developer}/{app}.json"
USERROLES_SNAPSHOT_TARGET_SUBPATH = "snapshots/userroles/userroles.json"
USERROLES_FOR_A_ROLE_TARGET_SUBPATH = "userroles/{role_name}/users.json"
RESOURCE_PERMISSIONS_TARGET_SUBPATH = "userroles/{role_name}/resource_permissions.json"


@dataclass
class BackupConfig:
    api_choices: Set[str]
    authentication: Struct
    environments: List[str]
    org_name: str
    prefix: Optional[str]
    working_directory: str
    progress_bar: Any = None
    snapshot_data: Struct = empty_snapshot()
    snapshot_size: int = 0
    working_org_directory: Optional[Path] = None

    def __post_init__(self):
        if not isinstance(self.api_choices, set):
            self.api_choices = set(self.api_choices) if self.api_choices else APIGEE_API_CHOICES

        self.api_choices = sorted(self.api_choices)
        
        if self.environments is None:
            self.environments = []
        
        self.working_directory = get_resolved_directory_path(self.working_directory)
        self.working_org_directory = Path(self.working_directory) / self.org_name


class Backups:
    def __init__(self, config: BackupConfig):
        self.backupConfig = config

    def calculate_total_snapshot_size(self):
        total_size = 0
        for data in self.backupConfig.snapshot_data.__dict__:
            if data == "apis":
                total_size += len(self.backupConfig.snapshot_data.apis)
            elif data in ("keyvaluemaps", "targetservers", "caches"):
                for _, environment_data in self.backupConfig.snapshot_data.__dict__[data].items():
                    total_size += len(environment_data)
            elif data == "apps":
                for _, apps in self.backupConfig.snapshot_data.apps.items():
                    total_size += len(apps)
            elif isinstance(self.backupConfig.snapshot_data.__dict__[data], list):
                total_size += len(self.backupConfig.snapshot_data.__dict__[data])
        return total_size

    # GET (list) items from Apigee and write to files

    def fetch_and_generate_snapshots(self):
        for api_choice in self.backupConfig.api_choices:
            self.retrieve_listing(api_choice)
            self.create_snapshot(api_choice)
            console.echo("Done")
        self.backupConfig.snapshot_size = self.calculate_total_snapshot_size()

    def retrieve_listing(self, api_choice):
        if api_choice in ("apis", "apps"):
            console.echo(
                f"Retrieving {api_choice} listing (this may take a while)... ",
                line_ending="",
                should_flush=True,
            )
        else:
            console.echo(
                f"Retrieving {api_choice} listing... ",
                line_ending="",
                should_flush=True,
            )

    def create_snapshot(self, api_choice):
        getattr(self, f"create_{api_choice}_snapshot")()

    # GET (get) configs from Apigee and write to files

    def generate_snapshot_files_and_download_data(self):
        self.fetch_and_generate_snapshots()
        self.generate_snapshot_files()
        self.close_progress_bar()
        console.echo("Done.")

    def generate_snapshot_files(self):
        console.echo("Generating snapshot files...")
        for api_choice in self.backupConfig.api_choices:
            getattr(self, f"download_and_save_{api_choice}")()

    def close_progress_bar(self):
        self.backupConfig.progress_bar.close()

    # write configs to file

    def save_content_to_file(self, content, subpath):
        fullpath = self.get_full_path(self.backupConfig.working_org_directory, subpath)
        write_content_to_file(content, fullpath, indentation=2)

    def get_full_path(self, working_org_directory, subpath):
        fullpath = working_org_directory
        for level in subpath.split("/"):
            fullpath /= level
        return fullpath

    # update the download progress bar

    def update_progress_bar(self, description=""):
        self.initialize_progress_bar(self.backupConfig)
        self.set_progress_bar_description(self.backupConfig, description)
        self.increment_progress_bar(self.backupConfig)

    def initialize_progress_bar(self, backupConfig):
        if not isinstance(backupConfig.progress_bar, tqdm):
            backupConfig.progress_bar = tqdm(
                total=backupConfig.snapshot_size,
                unit="files",
                bar_format="{l_bar}{bar:32}{r_bar}{bar:-10b}",
                leave=False,
            )

    def set_progress_bar_description(self, backupConfig, description):
        if description:
            backupConfig.progress_bar.set_description(description)

    def increment_progress_bar(self, backupConfig):
        backupConfig.progress_bar.update(1)

    # api_proxies

    def create_apis_snapshot(self):
        api_proxies = self.list_api_proxies()
        self.backupConfig.snapshot_data.apis = self.get_api_details(api_proxies)
        self.save_apis_snapshot()

    def list_api_proxies(self):
        return Apis(
            self.backupConfig.authentication, self.backupConfig.org_name
        ).list_api_proxies(prefix=self.backupConfig.prefix, format="dict")

    def get_api_details(self, api_proxies):
        apis = {}
        for api in api_proxies:
            api_details = Apis(
                self.backupConfig.authentication,
                self.backupConfig.org_name
            ).get_api_proxy(api).json()
            apis[api] = api_details
        return apis

    def save_apis_snapshot(self):
        for api, content in self.backupConfig.snapshot_data.apis.items():
            path = APIS_SNAPSHOT_TARGET_SUBPATH.format(
                org_path=self.backupConfig.working_org_directory,
                api=api
            )
            self.save_content_to_file(content, path)

    # apiproducts

    def create_apiproducts_snapshot(self):
        apiproducts = self.list_api_products()
        self.backupConfig.snapshot_data.apiproducts = apiproducts
        self.save_apiproducts_snapshot()

    def list_api_products(self):
        return Apiproducts(
            self.backupConfig.authentication, self.backupConfig.org_name, None
        ).list_api_products(prefix=self.backupConfig.prefix, format="dict")

    def save_apiproducts_snapshot(self):
        content = self.backupConfig.snapshot_data.apiproducts
        self.save_content_to_file(content, APIPRODUCTS_SNAPSHOT_TARGET_SUBPATH)

    # apps

    def create_apps_snapshot(self, expand=False, count=1000, startkey=""):
        developers = self.list_all_developers(expand=expand, count=count, startkey=startkey)
        self.backupConfig.snapshot_data.apps = self.list_apps_for_developers(developers)
        self.backupConfig.snapshot_data.apps = self.filter_empty_values(self.backupConfig.snapshot_data.apps)
        self.save_apps_snapshot()

    def list_all_developers(self, expand=False, count=1000, startkey=""):
        return Developers(
            self.backupConfig.authentication, self.backupConfig.org_name, None
        ).list_developers(
            prefix=None,
            expand=expand,
            count=count,
            startkey=startkey,
            format="dict",
        )

    def list_apps_for_developers(self, developers):
        return Apps(
            self.backupConfig.authentication, self.backupConfig.org_name, None
        ).list_apps_for_all_developers(
            developers,
            prefix=self.backupConfig.prefix,
            format="dict",
        )

    def filter_empty_values(self, apps):
        return filter_out_empty_values(apps)

    def save_apps_snapshot(self):
        for app_name, details in self.backupConfig.snapshot_data.apps.items():
            self.save_content_to_file(details, APPS_SNAPSHOT_TARGET_SUBPATH.format(app=app_name))

    # caches

    def create_caches_snapshot(self):
        for environment in self.backupConfig.environments:
            caches = self.list_caches_in_environment(environment)
            self.backupConfig.snapshot_data.caches[environment] = caches
            self.save_caches_snapshot(environment)

    def list_caches_in_environment(self, environment):
        return Caches(
            self.backupConfig.authentication, self.backupConfig.org_name, None
        ).list_caches_in_an_environment(
            environment, prefix=self.backupConfig.prefix, format="dict"
        )

    def save_caches_snapshot(self, environment):
        content = self.backupConfig.snapshot_data.caches[environment]
        path = CACHES_SNAPSHOT_TARGET_SUBPATH.format(environment=environment)
        self.save_content_to_file(content, path)

    # developers

    def create_developers_snapshot(self):
        self.backupConfig.snapshot_data.developers = Developers(
            self.backupConfig.authentication, self.backupConfig.org_name, None
        ).list_developers(prefix=self.backupConfig.prefix, format="dict")
        content = self.backupConfig.snapshot_data.developers
        self.save_content_to_file(content, DEVELOPERS_SNAPSHOT_TARGET_SUBPATH)

    # keyvaluemaps

    def create_keyvaluemaps_snapshot(self):
        for environment in self.backupConfig.environments:
            keyvaluemaps = self.list_keyvaluemaps_in_environment(environment)
            self.backupConfig.snapshot_data.keyvaluemaps[environment] = keyvaluemaps
            self.save_keyvaluemaps_snapshot(environment)

    def list_keyvaluemaps_in_environment(self, environment):
        return Keyvaluemaps(
            self.backupConfig.authentication, self.backupConfig.org_name, None
        ).list_keyvaluemaps_in_an_environment(
            environment, prefix=self.backupConfig.prefix, format="dict"
        )

    def save_keyvaluemaps_snapshot(self, environment):
        content = self.backupConfig.snapshot_data.keyvaluemaps[environment]
        path = KEYVALUEMAPS_SNAPSHOT_TARGET_SUBPATH.format(environment=environment)
        self.save_content_to_file(content, path)

    # targetservers

    def create_targetservers_snapshot(self):
        for environment in self.backupConfig.environments:
            targetservers = self.list_targetservers_in_environment(environment)
            self.backupConfig.snapshot_data.targetservers[environment] = targetservers
            self.save_targetservers_snapshot(environment)

    def list_targetservers_in_environment(self, environment):
        return Targetservers(
            self.backupConfig.authentication, self.backupConfig.org_name, None
        ).list_targetservers_in_an_environment(
            environment, prefix=self.backupConfig.prefix, format="dict"
        )

    def save_targetservers_snapshot(self, environment):
        content = self.backupConfig.snapshot_data.targetservers[environment]
        path = TARGETSERVERS_SNAPSHOT_TARGET_SUBPATH.format(environment=environment)
        self.save_content_to_file(content, path)

    # userroles

    def create_userroles_snapshot(self):
        userroles = self.list_user_roles()
        userroles_filtered = self.filter_userroles(userroles)
        self.backupConfig.snapshot_data.userroles = userroles_filtered
        self.save_userroles_snapshot()

    def list_user_roles(self):
        return (
            Userroles(
                self.backupConfig.authentication, self.backupConfig.org_name, None
            )
            .list_user_roles()
            .json()
        )

    def filter_userroles(self, userroles):
        return (
            [
                role
                for role in userroles
                if role.startswith(self.backupConfig.prefix)
            ]
            if self.backupConfig.prefix
            else userroles
        )

    def save_userroles_snapshot(self):
        content = self.backupConfig.snapshot_data.userroles
        self.save_content_to_file(content, USERROLES_SNAPSHOT_TARGET_SUBPATH)


    # apis

    def download_and_save_apis(self):
        for api, metadata in self.backupConfig.snapshot_data.apis.items():
            for revision in metadata["revision"]:
                output_file = self.get_output_file_path(api, revision)
                work_dir = os.path.dirname(output_file)
                try:
                    self.export_and_extract_api(api, revision, output_file, work_dir)
                except HTTPError as e:
                    self.handle_api_export_error(e, api, revision)
                except Exception as e:
                    self.handle_general_exception(type(e).__name__, api, revision)
            self.update_progress_bar(description="APIs")

    def get_output_file_path(self, api, revision):
        return str(
            Path(self.backupConfig.working_org_directory)
            / "apis"
            / api
            / revision
            / f"{api}.zip"
        )

    def export_and_extract_api(self, api, revision, output_file, work_dir):
        Apis(
            self.backupConfig.authentication,
            self.backupConfig.org_name
        ).export_api_proxy(
            api,
            revision,
            write_to_filesystem=True,
            output_file=output_file
        )
        extract_zip_file(output_file, work_dir)
        os.remove(output_file)

    def handle_api_export_error(self, error, api, revision):
        log_and_echo_http_error(error, append_message=f" for API Proxy ({api}, revision {revision})")

    # apiproducts

    def download_and_save_apiproducts(self):
        for apiproduct in self.backupConfig.snapshot_data.apiproducts:
            try:
                content = self.get_apiproduct_content(apiproduct)
                path = self.get_apiproduct_path(apiproduct)
                self.save_content_to_file(content, path)
            except HTTPError as e:
                self.handle_apiproduct_download_error(e, apiproduct)
            except Exception as e:
                self.handle_general_exception(type(e).__name__, apiproduct)
            self.update_progress_bar(description="API Products")

    def get_apiproduct_content(self, apiproduct):
        content = (
            Apiproducts(
                self.backupConfig.authentication,
                self.backupConfig.org_name,
                apiproduct
            )
            .get_api_product()
            .text
        )
        return content

    def get_apiproduct_path(self, apiproduct):
        return APIPRODUCTS_TARGET_SUBPATH.format(apiproduct=apiproduct)

    def handle_apiproduct_download_error(self, error, apiproduct):
        log_and_echo_http_error(error, append_message=f" for API Product ({apiproduct})")

    # apps

    def download_and_save_apps(self):
        for developer, apps in self.backupConfig.snapshot_data.apps.items():
            for app in apps:
                try:
                    content = self.get_developer_app_details(developer, app)
                    path = self.get_app_path(developer, app)
                    self.save_content_to_file(content, path)
                except HTTPError as e:
                    self.handle_app_download_error(e, app)
                except Exception as e:
                    self.handle_general_exception(e, developer, app)
                self.update_progress_bar(description="Developer Apps")

    def get_developer_app_details(self, developer, app):
        content = (
            Apps(
                self.backupConfig.authentication,
                self.backupConfig.org_name,
                app
            )
            .get_developer_app_details(developer)
            .text
        )
        return content

    def get_app_path(self, developer, app):
        return APPS_TARGET_SUBPATH.format(developer=developer, app=app)

    def handle_app_download_error(self, error, app):
        log_and_echo_http_error(error, append_message=f" for Developer App ({app})")

    def handle_general_exception(self, error, *args):
        console.echo(type(error).__name__, *args)

    # caches

    def download_and_save_caches(self):
        for environment in self.backupConfig.environments:
            caches = self.backupConfig.snapshot_data.caches[environment]
            for cache in caches:
                try:
                    content = self.get_cache_information(environment, cache)
                    path = self.get_cache_path(environment, cache)
                    self.save_content_to_file(content, path)
                except HTTPError as e:
                    self.handle_cache_download_error(e, cache)
                except Exception as e:
                    self.handle_general_exception(e, environment, cache)
                self.update_progress_bar(description="Caches")

    def get_cache_information(self, environment, cache):
        content = (
            Caches(
                self.backupConfig.authentication,
                self.backupConfig.org_name,
                cache
            )
            .get_information_about_a_cache(environment)
            .text
        )
        return content

    def get_cache_path(self, environment, cache):
        return CACHES_TARGET_SUBPATH.format(environment=environment, cache=cache)

    def handle_cache_download_error(self, error, cache):
        log_and_echo_http_error(error, append_message=f" for Cache ({cache})")

    # developers

    def download_and_save_developers(self):
        for developer in self.backupConfig.snapshot_data.developers:
            try:
                content = self.get_developer_details(developer)
                path = self.get_developer_path(developer)
                self.save_content_to_file(content, path)
            except HTTPError as e:
                self.handle_developer_download_error(e, developer)
            except Exception as e:
                self.handle_general_exception(e, developer)
            self.update_progress_bar(description="Developers")

    def get_developer_details(self, developer):
        content = (
            Developers(
                self.backupConfig.authentication,
                self.backupConfig.org_name,
                developer
            )
            .get_developer()
            .text
        )
        return content

    def get_developer_path(self, developer):
        return DEVELOPERS_TARGET_SUBPATH.format(developer=developer)

    def handle_developer_download_error(self, error, developer):
        log_and_echo_http_error(error, append_message=f" for Developer ({developer})")

    # keyvaluemaps

    def download_and_save_keyvaluemaps(self):
        for environment in self.backupConfig.environments:
            keyvaluemaps = self.backupConfig.snapshot_data.keyvaluemaps[environment]
            for kvm in keyvaluemaps:
                try:
                    content = self.get_keyvaluemap_content(environment, kvm)
                    path = self.get_keyvaluemap_path(environment, kvm)
                    self.save_content_to_file(content, path)
                except HTTPError as e:
                    self.handle_keyvaluemap_download_error(e, kvm)
                except Exception as e:
                    self.handle_general_exception(e, environment, kvm)
                self.update_progress_bar(description="KeyValueMaps")

    def get_keyvaluemap_content(self, environment, kvm):
        content = (
            Keyvaluemaps(
                self.backupConfig.authentication,
                self.backupConfig.org_name,
                kvm
            )
            .get_keyvaluemap_in_an_environment(environment)
            .text
        )
        return content

    def get_keyvaluemap_path(self, environment, kvm):
        return KEYVALUEMAPS_TARGET_SUBPATH.format(environment=environment, kvm=kvm)

    def handle_keyvaluemap_download_error(self, error, kvm):
        log_and_echo_http_error(error, append_message=f" for KVM ({kvm})")

    # targetservers

    def download_and_save_targetservers(self):
        for environment in self.backupConfig.environments:
            targetservers = self.backupConfig.snapshot_data.targetservers[environment]
            for targetserver in targetservers:
                try:
                    content = self.get_targetserver_content(environment, targetserver)
                    path = self.get_targetserver_path(environment, targetserver)
                    self.save_content_to_file(content, path)
                except HTTPError as e:
                    self.handle_targetserver_download_error(e, targetserver)
                except Exception as e:
                    self.handle_general_exception(e, environment, targetserver)
                self.update_progress_bar(description="TargetServers")

    def get_targetserver_content(self, environment, targetserver):
        content = (
            Targetservers(
                self.backupConfig.authentication,
                self.backupConfig.org_name,
                targetserver
            )
            .get_targetserver(environment)
            .text
        )
        return content

    def get_targetserver_path(self, environment, targetserver):
        return TARGETSERVERS_TARGET_SUBPATH.format(
            environment=environment, targetserver=targetserver
        )

    def handle_targetserver_download_error(self, error, targetserver):
        log_and_echo_http_error(error, append_message=f" for TargetServer ({targetserver})")

    # userroles

    def download_and_save_userroles(self):
        for role_name in self.backupConfig.snapshot_data.userroles:
            try:
                self.backupConfig.download_users_for_a_role(role_name)
            except HTTPError as e:
                log_and_echo_http_error(e, append_message=" for User Role ({role_name}) users")
            except Exception as e:
                self.handle_general_exception(e, role_name)
            try:
                self.backupConfig.download_resource_permissions(role_name)
            except HTTPError as e:
                log_and_echo_http_error(e, append_message=" for User Role ({role_name}) resource permissions")  
            except Exception as e:
                self.handle_general_exception(e, role_name, "(resource permissions)")
            self.update_progress_bar(description="User Roles")

    def download_users_for_a_role(self, role_name):
        content = self.get_users_for_a_role_content(role_name)
        path = USERROLES_FOR_A_ROLE_TARGET_SUBPATH.format(role_name=role_name)
        self.save_content_to_file(content, path)

    def download_resource_permissions(self, role_name):
        content = self.get_resource_permissions_content(role_name)
        path = RESOURCE_PERMISSIONS_TARGET_SUBPATH.format(role_name=role_name)
        self.save_content_to_file(content, path)

    def get_users_for_a_role_content(self, role_name):
        return (
            Userroles(
                self.backupConfig.authentication,
                self.backupConfig.org_name,
                role_name,
            )
            .get_users_for_a_role()
            .json()
        )

    def get_resource_permissions_content(self, role_name):
        permissions = Permissions(
            self.backupConfig.authentication,
            self.backupConfig.org_name,
            role_name
        ).get_permissions(formatted=True, format="json")
        content = Userroles.sort_resource_permissions(permissions)
        return json.dumps(content, indent=2)
