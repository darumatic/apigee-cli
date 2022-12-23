import json
import logging
import os
from pathlib import Path

from requests.exceptions import HTTPError
from tqdm import tqdm

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.apiproducts.apiproducts import Apiproducts
from apigee.apis.apis import Apis
from apigee.apps.apps import Apps
from apigee.caches.caches import Caches
from apigee.developers.developers import Developers
from apigee.exceptions import InvalidApisError
from apigee.keyvaluemaps.keyvaluemaps import Keyvaluemaps
from apigee.permissions.permissions import Permissions
from apigee.targetservers.targetservers import Targetservers
from apigee.types import APIS, Struct, empty_snapshot
from apigee.userroles.userroles import Userroles
from apigee.utils import (
    build_path_str,
    extract_zip,
    resolve_target_directory,
    touch,
    write_file,
)

APIS_SNAPSHOT_SUBPATH = "snapshots/apis/{api}.json"
# APIS_SUBPATH = 'apis/{api}/revision/{api}.zip'
KEYVALUEMAPS_SNAPSHOT_SUBPATH = "snapshots/keyvaluemaps/{environment}/keyvaluemaps.json"
KEYVALUEMAPS_SUBPATH = "keyvaluemaps/{environment}/{kvm}.json"
TARGETSERVERS_SNAPSHOT_SUBPATH = (
    "snapshots/targetservers/{environment}/targetservers.json"
)
TARGETSERVERS_SUBPATH = "targetservers/{environment}/{targetserver}.json"
CACHES_SNAPSHOT_SUBPATH = "snapshots/caches/{environment}/caches.json"
CACHES_SUBPATH = "caches/{environment}/{cache}.json"
DEVELOPERS_SNAPSHOT_SUBPATH = "snapshots/developers/developers.json"
DEVELOPERS_SUBPATH = "developers/{developer}.json"
APIPRODUCTS_SNAPSHOT_SUBPATH = "snapshots/apiproducts/apiproducts.json"
APIPRODUCTS_SUBPATH = "apiproducts/{apiproduct}.json"
APPS_SNAPSHOT_SUBPATH = "snapshots/apps/{app}.json"
APPS_SUBPATH = "apps/{developer}/{app}.json"
USERROLES_SNAPSHOT_SUBPATH = "snapshots/userroles/userroles.json"
USERROLES_FOR_A_ROLE_SUBPATH = "userroles/{role_name}/users.json"
RESOURCE_PERMISSIONS_SUBPATH = "userroles/{role_name}/resource_permissions.json"


class Backups:
    def __init__(self, auth, org_name, work_dir, prefix=None, apis=APIS, envs=[]):
        self.auth = auth
        self.org_name = org_name
        self.work_dir = resolve_target_directory(work_dir)
        self.prefix = prefix
        # self.fs_write = fs_write
        if not isinstance(apis, set):
            apis = set(apis)
        self.apis = sorted(apis)
        self.environments = envs
        self.snapshot_data = empty_snapshot()
        self.snapshot_size = 0
        self.progress_bar = None
        self.org_path = Path(self.work_dir) / self.org_name

    @property
    def apis(self):
        return self._apis

    @apis.setter
    def apis(self, value):
        if not value:
            raise InvalidApisError
        for t in value:
            if t not in APIS:
                raise InvalidApisError
        self._apis = value

    @staticmethod
    def log_error(error, append_msg=""):
        error_message = f"Ignoring {type(error).__name__} {error.response.status_code} error{append_msg}"
        logging.warning(error_message)
        console.echo(error_message)

    def update_progress(self, desc=""):
        if not isinstance(self.progress_bar, tqdm):
            self.progress_bar = tqdm(
                total=self.snapshot_size,
                unit="files",
                bar_format="{l_bar}{bar:32}{r_bar}{bar:-10b}",
                leave=False,
            )
        if desc:
            self.progress_bar.set_description(desc)
        self.progress_bar.update(1)

    def save(self, content, subpath):
        fullpath = self.org_path
        for level in subpath.split("/"):
            fullpath /= level
        write_file(content, fullpath, indent=2)

    def download_apis_snapshot(self):
        for api in Apis(self.auth, self.org_name).list_api_proxies(
            prefix=self.prefix, format="dict"
        ):
            self.snapshot_data.apis[api] = (
                Apis(self.auth, self.org_name).get_api_proxy(api).json()
            )
            content = self.snapshot_data.apis[api]
            path = APIS_SNAPSHOT_SUBPATH.format(org_path=self.org_path, api=api)
            self.save(content, path)

    def download_apis(self):
        for api, metadata in self.snapshot_data.apis.items():
            for revision in metadata["revision"]:
                output_file = str(
                    Path(self.org_path) / "apis" / api / revision / f"{api}.zip"
                )
                work_dir = os.path.dirname(output_file)
                try:
                    Apis(self.auth, self.org_name).export_api_proxy(
                        api, revision, fs_write=True, output_file=output_file
                    )
                    extract_zip(output_file, work_dir)
                    os.remove(output_file)
                except HTTPError as e:
                    Backups.log_error(
                        e, append_msg=" for API Proxy ({api}, revision {revision})"
                    )
            self.update_progress(desc="APIs")

    def download_keyvaluemaps_snapshot(self):
        for environment in self.environments:
            self.snapshot_data.keyvaluemaps[environment] = Keyvaluemaps(
                self.auth, self.org_name, None
            ).list_keyvaluemaps_in_an_environment(
                environment, prefix=self.prefix, format="dict"
            )
            content = self.snapshot_data.keyvaluemaps[environment]
            path = KEYVALUEMAPS_SNAPSHOT_SUBPATH.format(environment=environment)
            self.save(content, path)

    def download_keyvaluemaps(self):
        for environment in self.environments:
            for kvm in self.snapshot_data.keyvaluemaps[environment]:
                try:
                    content = (
                        Keyvaluemaps(self.auth, self.org_name, kvm)
                        .get_keyvaluemap_in_an_environment(environment)
                        .text
                    )
                    path = KEYVALUEMAPS_SUBPATH.format(environment=environment, kvm=kvm)
                    self.save(content, path)
                except HTTPError as e:
                    Backups.log_error(e, append_msg=" for KVM ({kvm})")
                self.update_progress(desc="KeyValueMaps")

    def download_targetservers_snapshot(self):
        for environment in self.environments:
            self.snapshot_data.targetservers[environment] = Targetservers(
                self.auth, self.org_name, None
            ).list_targetservers_in_an_environment(
                environment, prefix=self.prefix, format="dict"
            )
            content = self.snapshot_data.targetservers[environment]
            path = TARGETSERVERS_SNAPSHOT_SUBPATH.format(environment=environment)
            self.save(content, path)

    def download_targetservers(self):
        for environment in self.environments:
            for targetserver in self.snapshot_data.targetservers[environment]:
                try:
                    content = (
                        Targetservers(self.auth, self.org_name, targetserver)
                        .get_targetserver(environment)
                        .text
                    )
                    path = TARGETSERVERS_SUBPATH.format(
                        environment=environment, targetserver=targetserver
                    )
                    self.save(content, path)
                except HTTPError as e:
                    Backups.log_error(
                        e, append_msg=" for TargetServer ({targetserver})"
                    )
                self.update_progress(desc="TargetServers")

    def download_caches_snapshot(self):
        for environment in self.environments:
            self.snapshot_data.caches[environment] = Caches(
                self.auth, self.org_name, None
            ).list_caches_in_an_environment(
                environment, prefix=self.prefix, format="dict"
            )
            content = self.snapshot_data.caches[environment]
            path = CACHES_SNAPSHOT_SUBPATH.format(environment=environment)
            self.save(content, path)

    def download_caches(self):
        for environment in self.environments:
            for cache in self.snapshot_data.caches[environment]:
                try:
                    content = (
                        Caches(self.auth, self.org_name, cache)
                        .get_information_about_a_cache(environment)
                        .text
                    )
                    path = CACHES_SUBPATH.format(environment=environment, cache=cache)
                    self.save(content, path)
                except HTTPError as e:
                    Backups.log_error(e, append_msg=" for Cache ({cache})")
                self.update_progress(desc="Caches")

    def download_developers_snapshot(self):
        self.snapshot_data.developers = Developers(
            self.auth, self.org_name, None
        ).list_developers(prefix=self.prefix, format="dict")
        content = self.snapshot_data.developers
        self.save(content, DEVELOPERS_SNAPSHOT_SUBPATH)

    def download_developers(self):
        for developer in self.snapshot_data.developers:
            try:
                content = (
                    Developers(self.auth, self.org_name, developer).get_developer().text
                )
                path = DEVELOPERS_SUBPATH.format(developer=developer)
                self.save(content, path)
            except HTTPError as e:
                Backups.log_error(e, append_msg=" for Developer ({developer})")
            self.update_progress(desc="Developers")

    def download_apiproducts_snapshot(self):
        self.snapshot_data.apiproducts = Apiproducts(
            self.auth, self.org_name, None
        ).list_api_products(prefix=self.prefix, format="dict")
        content = self.snapshot_data.apiproducts
        self.save(content, APIPRODUCTS_SNAPSHOT_SUBPATH)

    def download_apiproducts(self):
        for apiproduct in self.snapshot_data.apiproducts:
            try:
                content = (
                    Apiproducts(self.auth, self.org_name, apiproduct)
                    .get_api_product()
                    .text
                )
                path = APIPRODUCTS_SUBPATH.format(apiproduct=apiproduct)
                self.save(content, path)
            except HTTPError as e:
                Backups.log_error(e, append_msg=" for API Product ({apiproduct})")
            self.update_progress(desc="API Products")

    def download_apps_snapshot(self, expand=False, count=1000, startkey=""):
        self.snapshot_data.apps = Apps(
            self.auth, self.org_name, None
        ).list_apps_for_all_developers(
            Developers(self.auth, self.org_name, None).list_developers(
                prefix=None,
                expand=expand,
                count=count,
                startkey=startkey,
                format="dict",
            ),
            prefix=self.prefix,
            format="dict",
        )
        self.snapshot_data.apps = {
            k: v for k, v in self.snapshot_data.apps.items() if v
        }
        for app, details in self.snapshot_data.apps.items():
            self.save(details, APPS_SNAPSHOT_SUBPATH)

    def download_apps(self):
        for developer, apps in self.snapshot_data.apps.items():
            for app in apps:
                try:
                    content = (
                        Apps(self.auth, self.org_name, app)
                        .get_developer_app_details(developer)
                        .text
                    )
                    path = APPS_SUBPATH.format(developer=developer, app=app)
                    self.save(content, path)
                except HTTPError as e:
                    Backups.log_error(e, append_msg=" for Developer App ({app})")
                self.update_progress(desc="Developer Apps")

    def download_userroles_snapshot(self):
        self.snapshot_data.userroles = (
            Userroles(self.auth, self.org_name, None).list_user_roles().json()
        )
        if self.prefix:
            self.snapshot_data.userroles = [
                role
                for role in self.snapshot_data.userroles
                if role.startswith(self.prefix)
            ]
        self.save(self.snapshot_data.userroles, USERROLES_SNAPSHOT_SUBPATH)

    def download_userroles(self):
        for role_name in self.snapshot_data.userroles:
            self.download_users_for_a_role(role_name)
            self.download_resource_permissions(role_name)
            self.update_progress(desc="User Roles")

    def download_users_for_a_role(self, role_name):
        try:
            content = (
                Userroles(self.auth, self.org_name, role_name)
                .get_users_for_a_role()
                .json()
            )
            path = USERROLES_FOR_A_ROLE_SUBPATH.format(role_name=role_name)
            self.save(content, path)
        except HTTPError as e:
            Backups.log_error(e, append_msg=" for User Role ({role_name}) users")

    def download_resource_permissions(self, role_name):
        try:
            permissions = Permissions(
                self.auth, self.org_name, role_name
            ).get_permissions(formatted=True, format="json")
            content = Userroles.sort_permissions(permissions)
            path = RESOURCE_PERMISSIONS_SUBPATH.format(role_name=role_name)
            self.save(json.dumps(content, indent=2), path)
        except HTTPError as e:
            Backups.log_error(
                e, append_msg=" for User Role ({role_name}) resource permissions"
            )

    def calculate_snapshot_size(self):
        count = 0
        for data in self.snapshot_data.__dict__:
            if data == "apis":
                count += len(self.snapshot_data.apis)
            elif data in ("keyvaluemaps", "targetservers", "caches"):
                for environment_bound_api, listing in self.snapshot_data.__dict__[
                    data
                ].items():
                    count += len(listing)
            elif data == "apps":
                for developer, apps in self.snapshot_data.apps.items():
                    count += len(apps)
            elif isinstance(self.snapshot_data.__dict__[data], list):
                count += len(self.snapshot_data.__dict__[data])
        return count

    def get_snapshots(self):
        for api in self.apis:
            if api in {"apis", "apps"}:
                console.echo(
                    f"Retrieving {api} listing (this may take a while)... ",
                    end="",
                    flush=True,
                )
            else:
                console.echo(f"Retrieving {api} listing... ", end="", flush=True)
            getattr(self, f"download_{api}_snapshot")()
            console.echo("Done")
        self.snapshot_size = self.calculate_snapshot_size()

    def take_snapshot(self):
        self.get_snapshots()
        console.echo("Generating snapshot files...")
        for api in self.apis:
            getattr(self, f"download_{api}")()
        self.progress_bar.close()
        console.echo("Done.")
