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

    def fetch_and_generate_snapshots(self):
        for api_choice in self.backupConfig.api_choices:
            if api_choice in {"apis", "apps"}:
                console.echo(
                    f"Retrieving {api_choice} listing (this may take a while)... ",
                    line_ending="",
                    should_flush=True,
                )
            else:
                console.echo(f"Retrieving {api_choice} listing... ", line_ending="", should_flush=True)
            getattr(self, f"create_{api_choice}_snapshot")()
            console.echo("Done")
        self.backupConfig.snapshot_size = self.calculate_total_snapshot_size()

    def generate_snapshot_files_and_download_data(self):
        self.fetch_and_generate_snapshots()
        console.echo("Generating snapshot files...")
        for api_choice in self.backupConfig.api_choices:
            getattr(self, f"download_and_save_{api_choice}")()
        self.backupConfig.progress_bar.close()
        console.echo("Done.")

    def save_content_to_file(self, content, subpath):
        fullpath = self.backupConfig.working_org_directory
        for level in subpath.split("/"):
            fullpath /= level
        write_content_to_file(content, fullpath, indentation=2)

    def update_progress_bar(self, description=""):
        if not isinstance(self.backupConfig.progress_bar, tqdm):
            self.backupConfig.progress_bar = tqdm(
                total=self.backupConfig.snapshot_size,
                unit="files",
                bar_format="{l_bar}{bar:32}{r_bar}{bar:-10b}",
                leave=False,
            )
        if description:
            self.backupConfig.progress_bar.set_description(description)
        self.backupConfig.progress_bar.update(1)

    # Start of methods to list items on Apigee

    def create_apiproducts_snapshot(self):
        self.backupConfig.snapshot_data.apiproducts = Apiproducts(
            self.backupConfig.authentication, self.backupConfig.org_name, None
        ).list_api_products(prefix=self.backupConfig.prefix, format="dict")
        content = self.backupConfig.snapshot_data.apiproducts
        self.save_content_to_file(content, APIPRODUCTS_SNAPSHOT_TARGET_SUBPATH)

    def create_apis_snapshot(self):
        for api in Apis(self.backupConfig.authentication, self.backupConfig.org_name).list_api_proxies(prefix=self.backupConfig.prefix, format="dict"):
            self.backupConfig.snapshot_data.apis[api] = Apis(self.backupConfig.authentication, self.backupConfig.org_name).get_api_proxy(api).json()
            content = self.backupConfig.snapshot_data.apis[api]
            path = APIS_SNAPSHOT_TARGET_SUBPATH.format(org_path=self.backupConfig.working_org_directory, api=api)
            self.save_content_to_file(content, path)

    def create_apps_snapshot(self, expand=False, count=1000, startkey=""):
        self.backupConfig.snapshot_data.apps = Apps(
            self.backupConfig.authentication, self.backupConfig.org_name, None
        ).list_apps_for_all_developers(
            Developers(self.backupConfig.authentication, self.backupConfig.org_name, None).list_developers(
                prefix=None,
                expand=expand,
                count=count,
                startkey=startkey,
                format="dict",
            ),
            prefix=self.backupConfig.prefix,
            format="dict",
        )
        self.backupConfig.snapshot_data.apps = filter_out_empty_values(self.backupConfig.snapshot_data.apps)
        for app_name, details in self.backupConfig.snapshot_data.apps.items():
            self.save_content_to_file(details, APPS_SNAPSHOT_TARGET_SUBPATH.format(app=app_name))

    def create_caches_snapshot(self):
        for environment in self.backupConfig.environments:
            self.backupConfig.snapshot_data.caches[environment] = Caches(
                self.backupConfig.authentication, self.backupConfig.org_name, None
            ).list_caches_in_an_environment(
                environment, prefix=self.backupConfig.prefix, format="dict"
            )
            content = self.backupConfig.snapshot_data.caches[environment]
            path = CACHES_SNAPSHOT_TARGET_SUBPATH.format(environment=environment)
            self.save_content_to_file(content, path)

    def create_developers_snapshot(self):
        self.backupConfig.snapshot_data.developers = Developers(
            self.backupConfig.authentication, self.backupConfig.org_name, None
        ).list_developers(prefix=self.backupConfig.prefix, format="dict")
        content = self.backupConfig.snapshot_data.developers
        self.save_content_to_file(content, DEVELOPERS_SNAPSHOT_TARGET_SUBPATH)

    def create_keyvaluemaps_snapshot(self):
        for environment in self.backupConfig.environments:
            self.backupConfig.snapshot_data.keyvaluemaps[environment] = Keyvaluemaps(
                self.backupConfig.authentication, self.backupConfig.org_name, None
            ).list_keyvaluemaps_in_an_environment(
                environment, prefix=self.backupConfig.prefix, format="dict"
            )
            content = self.backupConfig.snapshot_data.keyvaluemaps[environment]
            path = KEYVALUEMAPS_SNAPSHOT_TARGET_SUBPATH.format(environment=environment)
            self.save_content_to_file(content, path)

    def create_targetservers_snapshot(self):
        for environment in self.backupConfig.environments:
            self.backupConfig.snapshot_data.targetservers[environment] = Targetservers(
                self.backupConfig.authentication, self.backupConfig.org_name, None
            ).list_targetservers_in_an_environment(
                environment, prefix=self.backupConfig.prefix, format="dict"
            )
            content = self.backupConfig.snapshot_data.targetservers[environment]
            path = TARGETSERVERS_SNAPSHOT_TARGET_SUBPATH.format(environment=environment)
            self.save_content_to_file(content, path)

    def create_userroles_snapshot(self):
        self.backupConfig.snapshot_data.userroles = Userroles(self.backupConfig.authentication, self.backupConfig.org_name, None).list_user_roles().json()

        if self.backupConfig.prefix:
            self.backupConfig.snapshot_data.userroles = [role for role in self.backupConfig.snapshot_data.userroles if role.startswith(self.backupConfig.prefix)]

        self.save_content_to_file(self.backupConfig.snapshot_data.userroles, USERROLES_SNAPSHOT_TARGET_SUBPATH)

    # Start of methods to download configuration files from Apigee based on listed items

    def download_and_save_apis(self):
        for api, metadata in self.backupConfig.snapshot_data.apis.items():
            for revision in metadata["revision"]:
                output_file = str(Path(self.backupConfig.working_org_directory) / "apis" / api / revision / f"{api}.zip")
                work_dir = os.path.dirname(output_file)
                try:
                    Apis(self.backupConfig.authentication, self.backupConfig.org_name).export_api_proxy(api, revision, write_to_filesystem=True, output_file=output_file)
                    extract_zip_file(output_file, work_dir)
                    os.remove(output_file)
                except HTTPError as e:
                    log_and_echo_http_error(e, append_message=" for API Proxy ({api}, revision {revision})")
            self.update_progress_bar(description="APIs")

    def download_and_save_apiproducts(self):
        for apiproduct in self.backupConfig.snapshot_data.apiproducts:
            try:
                content = (
                    Apiproducts(self.backupConfig.authentication, self.backupConfig.org_name, apiproduct)
                    .get_api_product()
                    .text
                )
                path = APIPRODUCTS_TARGET_SUBPATH.format(apiproduct=apiproduct)
                self.save_content_to_file(content, path)
            except HTTPError as e:
                log_and_echo_http_error(e, append_message=" for API Product ({apiproduct})")
            self.update_progress_bar(description="API Products")

    def download_and_save_apps(self):
        for developer, apps in self.backupConfig.snapshot_data.apps.items():
            for app in apps:
                try:
                    content = (
                        Apps(self.backupConfig.authentication, self.backupConfig.org_name, app)
                        .get_developer_app_details(developer)
                        .text
                    )
                    path = APPS_TARGET_SUBPATH.format(developer=developer, app=app)
                    self.save_content_to_file(content, path)
                except HTTPError as e:
                    log_and_echo_http_error(e, append_message=" for Developer App ({app})")
                except Exception as e:
                    console.echo(type(e).__name__, developer, app)
                self.update_progress_bar(description="Developer Apps")

    def download_and_save_caches(self):
        for environment in self.backupConfig.environments:
            for cache in self.backupConfig.snapshot_data.caches[environment]:
                try:
                    content = (
                        Caches(self.backupConfig.authentication, self.backupConfig.org_name, cache)
                        .get_information_about_a_cache(environment)
                        .text
                    )
                    path = CACHES_TARGET_SUBPATH.format(environment=environment, cache=cache)
                    self.save_content_to_file(content, path)
                except HTTPError as e:
                    log_and_echo_http_error(e, append_message=" for Cache ({cache})")
                self.update_progress_bar(description="Caches")

    def download_and_save_developers(self):
        for developer in self.backupConfig.snapshot_data.developers:
            try:
                content = (
                    Developers(self.backupConfig.authentication, self.backupConfig.org_name, developer).get_developer().text
                )
                path = DEVELOPERS_TARGET_SUBPATH.format(developer=developer)
                self.save_content_to_file(content, path)
            except HTTPError as e:
                log_and_echo_http_error(e, append_message=" for Developer ({developer})")
            self.update_progress_bar(description="Developers")

    def download_and_save_keyvaluemaps(self):
        for environment in self.backupConfig.environments:
            for kvm in self.backupConfig.snapshot_data.keyvaluemaps[environment]:
                try:
                    content = (
                        Keyvaluemaps(self.backupConfig.authentication, self.backupConfig.org_name, kvm)
                        .get_keyvaluemap_in_an_environment(environment)
                        .text
                    )
                    path = KEYVALUEMAPS_TARGET_SUBPATH.format(environment=environment, kvm=kvm)
                    self.save_content_to_file(content, path)
                except HTTPError as e:
                    log_and_echo_http_error(e, append_message=" for KVM ({kvm})")
                self.update_progress_bar(description="KeyValueMaps")

    def download_and_save_targetservers(self):
        for environment in self.backupConfig.environments:
            for targetserver in self.backupConfig.snapshot_data.targetservers[environment]:
                try:
                    content = (
                        Targetservers(self.backupConfig.authentication, self.backupConfig.org_name, targetserver)
                        .get_targetserver(environment)
                        .text
                    )
                    path = TARGETSERVERS_TARGET_SUBPATH.format(
                        environment=environment, targetserver=targetserver
                    )
                    self.save_content_to_file(content, path)
                except HTTPError as e:
                    log_and_echo_http_error(
                        e, append_message=" for TargetServer ({targetserver})"
                    )
                self.update_progress_bar(description="TargetServers")

    def download_and_save_userroles(self):
        for role_name in self.backupConfig.snapshot_data.userroles:
            try:
                self.backupConfig.download_users_for_a_role(role_name)
            except HTTPError as e:
                log_and_echo_http_error(e, append_message=" for User Role ({role_name}) users")
            try:
                self.backupConfig.download_resource_permissions(role_name)
            except HTTPError as e:
                log_and_echo_http_error(e, append_message=" for User Role ({role_name}) resource permissions")  
            self.update_progress_bar(description="User Roles")

    def download_users_for_a_role(self, role_name):
        content = Userroles(self.backupConfig.authentication, self.backupConfig.org_name, role_name).get_users_for_a_role().json()
        path = USERROLES_FOR_A_ROLE_TARGET_SUBPATH.format(role_name=role_name)
        self.save_content_to_file(content, path)

    def download_resource_permissions(self, role_name):
        permissions = Permissions(self.backupConfig.authentication, self.backupConfig.org_name, role_name).get_permissions(formatted=True, format="json")
        content = Userroles.sort_resource_permissions(permissions)
        path = RESOURCE_PERMISSIONS_TARGET_SUBPATH.format(role_name=role_name)
        self.save_content_to_file(json.dumps(content, indent=2), path)
