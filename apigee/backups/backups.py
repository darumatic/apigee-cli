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
from apigee.exceptions import InvalidApisError, NotYetImplementedError
from apigee.keyvaluemaps.keyvaluemaps import Keyvaluemaps
from apigee.permissions.permissions import Permissions
from apigee.targetservers.targetservers import Targetservers
from apigee.types import APIS, Struct, empty_snapshot
from apigee.userroles.userroles import Userroles
from apigee.utils import (extract_zip, resolve_target_directory, touch,
                          write_file)


class Backups:
    def __init__(
        self,
        auth,
        org_name,
        target_directory,
        prefix=None,
        fs_write=False,
        apis=APIS,
        environments=['test', 'prod'],
    ):
        self.auth = auth
        self.org_name = org_name
        self.target_directory = resolve_target_directory(target_directory)
        self.prefix = prefix
        self.fs_write = fs_write
        if not isinstance(apis, set):
            apis = set(apis)
        self.apis = sorted(apis)
        self.environments = environments
        self.snapshot_data = empty_snapshot()
        self.snapshot_size = 0
        self.progress_bar = None
        self.org_path = Path(self.target_directory) / self.org_name

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
    def generate_download_path(root_path, is_snapshot=False, subpaths=[]):
        path = root_path
        if is_snapshot:
            path /= 'snapshots'
        for subpath in subpaths:
            path /= subpath
        return str(path)

    @staticmethod
    def log_error(error, append_msg=''):
        error_message = (
            f'Ignoring {type(error).__name__} {error.response.status_code} error' + append_msg
        )
        logging.warning(error_message)
        console.echo(error_message)

    def __progress_callback(self, desc=''):
        if not isinstance(self.progress_bar, tqdm):
            self.progress_bar = tqdm(
                total=self.snapshot_size,
                unit='files',
                bar_format='{l_bar}{bar:32}{r_bar}{bar:-10b}',
                leave=False,
            )
        if desc:
            self.progress_bar.set_description(desc)
        self.progress_bar.update(1)

    def download_apis_snapshot(self):
        for api in Apis(self.auth, self.org_name, None).list_api_proxies(
            prefix=self.prefix, format='dict'
        ):
            self.snapshot_data.apis[api] = (
                Apis(self.auth, self.org_name, None).get_api_proxy(api).json()
            )
            write_file(
                self.snapshot_data.apis[api],
                Backups.generate_download_path(
                    self.org_path, is_snapshot=True, subpaths=['apis', f'{api}.json']
                ),
                fs_write=self.fs_write,
                indent=2,
            )

    def download_apis(self):
        for api, metadata in self.snapshot_data.apis.items():
            for revision in metadata['revision']:
                output_file = Backups.generate_download_path(
                    self.org_path, subpaths=['apis', api, revision, f'{api}.zip']
                )
                target_directory = os.path.dirname(output_file)
                try:
                    Apis(self.auth, self.org_name, None).export_api_proxy(
                        api, revision, fs_write=True, output_file=output_file
                    )
                    extract_zip(output_file, target_directory)
                    os.remove(output_file)
                except HTTPError as e:
                    Backups.log_error(e, append_msg=' for API Proxy ({api}, revision {revision})')
            self._Backups__progress_callback(desc='APIs')

    def download_keyvaluemaps_snapshot(self):
        for environment in self.environments:
            self.snapshot_data.keyvaluemaps[environment] = Keyvaluemaps(
                self.auth, self.org_name, None
            ).list_keyvaluemaps_in_an_environment(environment, prefix=self.prefix, format='dict')
            write_file(
                self.snapshot_data.keyvaluemaps[environment],
                Backups.generate_download_path(
                    self.org_path,
                    is_snapshot=True,
                    subpaths=['keyvaluemaps', environment, 'keyvaluemaps.json'],
                ),
                fs_write=self.fs_write,
                indent=2,
            )

    def download_keyvaluemaps(self):
        for environment in self.environments:
            for kvm in self.snapshot_data.keyvaluemaps[environment]:
                try:
                    write_file(
                        Keyvaluemaps(self.auth, self.org_name, kvm)
                        .get_keyvaluemap_in_an_environment(environment)
                        .text,
                        Backups.generate_download_path(
                            self.org_path, subpaths=['keyvaluemaps', environment, f'{kvm}.json']
                        ),
                        fs_write=self.fs_write,
                    )
                except HTTPError as e:
                    Backups.log_error(e, append_msg=' for KVM ({kvm})')
                self._Backups__progress_callback(desc='KeyValueMaps')

    def download_targetservers_snapshot(self):
        for environment in self.environments:
            self.snapshot_data.targetservers[environment] = Targetservers(
                self.auth, self.org_name, None
            ).list_targetservers_in_an_environment(environment, prefix=self.prefix, format='dict')
            write_file(
                self.snapshot_data.targetservers[environment],
                Backups.generate_download_path(
                    self.org_path,
                    is_snapshot=True,
                    subpaths=['targetservers', environment, 'targetservers.json'],
                ),
                fs_write=self.fs_write,
                indent=2,
            )

    def download_targetservers(self):
        for environment in self.environments:
            for targetserver in self.snapshot_data.targetservers[environment]:
                try:
                    write_file(
                        Targetservers(self.auth, self.org_name, targetserver)
                        .get_targetserver(environment)
                        .text,
                        Backups.generate_download_path(
                            self.org_path,
                            subpaths=['targetservers', environment, f'{targetserver}.json'],
                        ),
                        fs_write=self.fs_write,
                    )
                except HTTPError as e:
                    Backups.log_error(e, append_msg=' for TargetServer ({targetserver})')
                self._Backups__progress_callback(desc='TargetServers')

    def download_caches_snapshot(self):
        for environment in self.environments:
            self.snapshot_data.caches[environment] = Caches(
                self.auth, self.org_name, None
            ).list_caches_in_an_environment(environment, prefix=self.prefix, format='dict')
            write_file(
                self.snapshot_data.caches[environment],
                Backups.generate_download_path(
                    self.org_path, is_snapshot=True, subpaths=['caches', environment, 'caches.json']
                ),
                fs_write=self.fs_write,
                indent=2,
            )

    def download_caches(self):
        for environment in self.environments:
            for cache in self.snapshot_data.caches[environment]:
                try:
                    write_file(
                        Caches(self.auth, self.org_name, cache)
                        .get_information_about_a_cache(environment)
                        .text,
                        Backups.generate_download_path(
                            self.org_path, subpaths=['caches', environment, f'{cache}.json']
                        ),
                        fs_write=self.fs_write,
                    )
                except HTTPError as e:
                    Backups.log_error(e, append_msg=' for Cache ({cache})')
                self._Backups__progress_callback(desc='Caches')

    def download_developers_snapshot(self):
        self.snapshot_data.developers = Developers(self.auth, self.org_name, None).list_developers(
            prefix=self.prefix, format='dict'
        )
        write_file(
            self.snapshot_data.developers,
            Backups.generate_download_path(
                self.org_path, is_snapshot=True, subpaths=['developers', 'developers.json']
            ),
            fs_write=self.fs_write,
            indent=2,
        )

    def download_developers(self):
        for developer in self.snapshot_data.developers:
            try:
                write_file(
                    Developers(self.auth, self.org_name, developer).get_developer().text,
                    Backups.generate_download_path(
                        self.org_path, subpaths=['developers', f'{developer}.json']
                    ),
                    fs_write=self.fs_write,
                )
            except HTTPError as e:
                Backups.log_error(e, append_msg=' for Developer ({developer})')
            self._Backups__progress_callback(desc='Developers')

    def download_apiproducts_snapshot(self):
        self.snapshot_data.apiproducts = Apiproducts(
            self.auth, self.org_name, None
        ).list_api_products(prefix=self.prefix, format='dict')
        write_file(
            self.snapshot_data.apiproducts,
            Backups.generate_download_path(
                self.org_path, is_snapshot=True, subpaths=['apiproducts', 'apiproducts.json']
            ),
            fs_write=self.fs_write,
            indent=2,
        )

    def download_apiproducts(self):
        for apiproduct in self.snapshot_data.apiproducts:
            try:
                write_file(
                    Apiproducts(self.auth, self.org_name, apiproduct).get_api_product().text,
                    Backups.generate_download_path(
                        self.org_path, subpaths=['apiproducts', f'{apiproduct}.json']
                    ),
                    fs_write=self.fs_write,
                )
            except HTTPError as e:
                Backups.log_error(e, append_msg=' for API Product ({apiproduct})')
            self._Backups__progress_callback(desc='API Products')

    def download_apps_snapshot(self, expand=False, count=1000, startkey=""):
        self.snapshot_data.apps = Apps(self.auth, self.org_name, None).list_apps_for_all_developers(
            Developers(self.auth, self.org_name, None).list_developers(
                prefix=None, expand=expand, count=count, startkey=startkey, format='dict'
            ),
            prefix=self.prefix,
            format='dict',
        )
        self.snapshot_data.apps = {k: v for k, v in self.snapshot_data.apps.items() if v}
        for app, details in self.snapshot_data.apps.items():
            write_file(
                details,
                Backups.generate_download_path(
                    self.org_path, is_snapshot=True, subpaths=['apps', f'{app}.json']
                ),
                fs_write=self.fs_write,
                indent=2,
            )

    def download_apps(self):
        for developer, apps in self.snapshot_data.apps.items():
            for app in apps:
                try:
                    write_file(
                        Apps(self.auth, self.org_name, app)
                        .get_developer_app_details(developer)
                        .text,
                        Backups.generate_download_path(
                            self.org_path, subpaths=['apps', developer, f'{app}.json']
                        ),
                        fs_write=self.fs_write,
                    )
                except HTTPError as e:
                    Backups.log_error(e, append_msg=' for Developer App ({app})')
                self._Backups__progress_callback(desc='Developer Apps')

    def download_userroles_snapshot(self):
        self.snapshot_data.userroles = (
            Userroles(self.auth, self.org_name, None).list_user_roles().json()
        )
        if self.prefix:
            self.snapshot_data.userroles = [
                role for role in self.snapshot_data.userroles if role.startswith(self.prefix)
            ]
        write_file(
            self.snapshot_data.userroles,
            Backups.generate_download_path(
                self.org_path, is_snapshot=True, subpaths=['userroles', 'userroles.json']
            ),
            fs_write=self.fs_write,
            indent=2,
        )

    def download_users_for_a_role(self, role_name):
        try:
            write_file(
                Userroles(self.auth, self.org_name, role_name).get_users_for_a_role().json(),
                Backups.generate_download_path(
                    self.org_path, subpaths=['userroles', role_name, 'users.json']
                ),
                fs_write=self.fs_write,
                indent=2,
            )
        except HTTPError as e:
            Backups.log_error(e, append_msg=' for User Role ({role_name}) users')

    def download_resource_permissions(self, role_name):
        try:
            write_file(
                json.dumps(
                    Userroles.sort_permissions(
                        Permissions(self.auth, self.org_name, role_name).get_permissions(
                            formatted=True, format='json'
                        )
                    ),
                    indent=2,
                ),
                Backups.generate_download_path(
                    self.org_path, subpaths=['userroles', role_name, 'resource_permissions.json']
                ),
                fs_write=self.fs_write,
            )
        except HTTPError as e:
            Backups.log_error(e, append_msg=' for User Role ({role_name}) resource permissions')

    def download_userroles(self):
        for role_name in self.snapshot_data.userroles:
            self.download_users_for_a_role(role_name)
            self.download_resource_permissions(role_name)
            self._Backups__progress_callback(desc='User Roles')

    def __calculate_snapshot_size(self):
        count = 0
        for x in self.snapshot_data.__dict__:
            if x == 'apis':
                count += len(self.snapshot_data.apis)
            elif x in ('keyvaluemaps', 'targetservers', 'caches'):
                for environment_bound_api, listing in self.snapshot_data.__dict__[x].items():
                    count += len(listing)
            elif x == 'apps':
                for developer, apps in self.snapshot_data.apps.items():
                    count += len(apps)
            elif isinstance(self.snapshot_data.__dict__[x], list):
                count += len(self.snapshot_data.__dict__[x])
        return count

    def get_snapshots(self):
        for api in self.apis:
            if api in {'apis', 'apps'}:
                console.echo(
                    f'Retrieving {api} listing (this may take a while)... ', end='', flush=True
                )
            else:
                console.echo(f'Retrieving {api} listing... ', end='', flush=True)
            getattr(self, f'download_{api}_snapshot')()
            console.echo('Done')
        self.snapshot_size = self._Backups__calculate_snapshot_size()

    def take_snapshot(self):
        self.get_snapshots()
        console.echo('Generating snapshot files...')
        for api in self.apis:
            getattr(self, f'download_{api}')()
        self.progress_bar.close()
        console.echo('Done.')
