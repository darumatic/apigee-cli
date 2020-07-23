import json
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
from apigee.types import Struct
from apigee.userroles.userroles import Userroles
from apigee.utils import (extract_zip, resolve_target_directory, touch,
                          write_file)


class Backups:

    APIS = {
        'apis',
        'keyvaluemaps',
        'targetservers',
        'caches',
        'developers',
        'apiproducts',
        'apps',
        'userroles',
    }
    SNAPSHOTS_DIRECTORY_NAME = 'snapshots'

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
        self.apis = apis
        self.environments = environments
        self.snapshot_data = Struct(
            apis={},
            keyvaluemaps={},
            targetservers={},
            caches={},
            developers=[],
            apps={},
            apiproducts=[],
            userroles=[],
        )
        self.snapshot_size = 0
        self.progress_bar = None

    # def __del__(self):
    #     if isinstance(self.progress_bar, tqdm):
    #         self.progress_bar.close()

    @property
    def apis(self):
        return self._apis

    @apis.setter
    def apis(self, value):
        if not value:
            raise InvalidApisError
        for t in value:
            if t not in self.APIS:
                raise InvalidApisError
        self._apis = value

    def _progress_callback(self, desc=''):
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
                str(
                    Path(self.target_directory)
                    / self.org_name
                    / self.SNAPSHOTS_DIRECTORY_NAME
                    / 'apis'
                    / (api + '.json')
                ),
                fs_write=self.fs_write,
            )
        return self.snapshot_data.apis

    def download_apis(self):
        for api, metadata in self.snapshot_data.apis.items():
            for revision in metadata['revision']:
                output_dir = str(
                    Path(self.target_directory) / self.org_name / 'apis' / api / revision
                )
                output_zip = str(Path(output_dir) / (api + '.zip'))
                try:
                    Apis(self.auth, self.org_name, None).export_api_proxy(
                        api, revision, fs_write=True, output_file=output_zip
                    )
                    extract_zip(output_zip, output_dir)
                    os.remove(output_zip)
                except HTTPError as e:
                    console.echo(
                        f'Ignoring {type(e).__name__} {e.response.status_code} error for API Proxy ({api}, revision {revision})'
                    )
            self._progress_callback(desc='APIs')
        return self.snapshot_data.apis

    def download_keyvaluemaps_snapshot(self):
        for environment in self.environments:
            try:
                self.snapshot_data.keyvaluemaps[environment] = Keyvaluemaps(
                    self.auth, self.org_name, None
                ).list_keyvaluemaps_in_an_environment(
                    environment, prefix=self.prefix, format='dict'
                )
            except HTTPError:
                self.snapshot_data.keyvaluemaps[environment] = []
            write_file(
                self.snapshot_data.keyvaluemaps[environment],
                str(
                    Path(self.target_directory)
                    / self.org_name
                    / self.SNAPSHOTS_DIRECTORY_NAME
                    / 'keyvaluemaps'
                    / environment
                    / 'keyvaluemaps.json'
                ),
                fs_write=self.fs_write,
            )
        return self.snapshot_data.keyvaluemaps

    def download_keyvaluemaps(self):
        for environment in self.environments:
            for kvm in self.snapshot_data.keyvaluemaps[environment]:
                try:
                    write_file(
                        Keyvaluemaps(self.auth, self.org_name, kvm)
                        .get_keyvaluemap_in_an_environment(environment)
                        .text,
                        str(
                            Path(self.target_directory)
                            / self.org_name
                            / 'keyvaluemaps'
                            / environment
                            / (kvm + '.json')
                        ),
                        fs_write=True,
                    )
                except HTTPError as e:
                    console.echo(
                        f'Ignoring {type(e).__name__} {e.response.status_code} error for KVM ({kvm})'
                    )
                self._progress_callback(desc='KeyValueMaps')
        return self.snapshot_data.keyvaluemaps

    def download_targetservers_snapshot(self):
        for environment in self.environments:
            try:
                self.snapshot_data.targetservers[environment] = Targetservers(
                    self.auth, self.org_name, None
                ).list_targetservers_in_an_environment(
                    environment, prefix=self.prefix, format='dict'
                )
            except HTTPError:
                self.snapshot_data.targetservers[environment] = []
            write_file(
                self.snapshot_data.targetservers[environment],
                str(
                    Path(self.target_directory)
                    / self.org_name
                    / self.SNAPSHOTS_DIRECTORY_NAME
                    / 'targetservers'
                    / environment
                    / 'targetservers.json'
                ),
                fs_write=self.fs_write,
            )
        return self.snapshot_data.targetservers

    def download_targetservers(self):
        for environment in self.environments:
            for targetserver in self.snapshot_data.targetservers[environment]:
                try:
                    write_file(
                        Targetservers(self.auth, self.org_name, targetserver)
                        .get_targetserver(environment)
                        .text,
                        str(
                            Path(self.target_directory)
                            / self.org_name
                            / 'targetservers'
                            / environment
                            / (targetserver + '.json')
                        ),
                        fs_write=True,
                    )
                except HTTPError as e:
                    console.echo(
                        f'Ignoring {type(e).__name__} {e.response.status_code} error for TargetServer ({targetserver})'
                    )
                self._progress_callback(desc='TargetServers')
        return self.snapshot_data.targetservers

    def download_caches_snapshot(self):
        for environment in self.environments:
            try:
                self.snapshot_data.caches[environment] = Caches(
                    self.auth, self.org_name, None
                ).list_caches_in_an_environment(environment, prefix=self.prefix, format='dict')
            except HTTPError:
                self.snapshot_data.caches[environment] = []
            write_file(
                self.snapshot_data.caches[environment],
                str(
                    Path(self.target_directory)
                    / self.org_name
                    / self.SNAPSHOTS_DIRECTORY_NAME
                    / 'caches'
                    / environment
                    / 'caches.json'
                ),
                fs_write=self.fs_write,
            )
        return self.snapshot_data.caches

    def download_caches(self):
        for environment in self.environments:
            for cache in self.snapshot_data.caches[environment]:
                try:
                    write_file(
                        Caches(self.auth, self.org_name, cache)
                        .get_information_about_a_cache(environment)
                        .text,
                        str(
                            Path(self.target_directory)
                            / self.org_name
                            / 'caches'
                            / environment
                            / (cache + '.json')
                        ),
                        fs_write=True,
                    )
                except HTTPError as e:
                    console.echo(
                        f'Ignoring {type(e).__name__} {e.response.status_code} error for Cache ({cache})'
                    )
                self._progress_callback(desc='Caches')
        return self.snapshot_data.caches

    def download_developers_snapshot(self):
        self.snapshot_data.developers = Developers(
            self.auth, self.org_name, None
        ).list_developers(prefix=self.prefix, format='dict')
        write_file(
            self.snapshot_data.developers,
            str(
                Path(self.target_directory)
                / self.org_name
                / self.SNAPSHOTS_DIRECTORY_NAME
                / 'developers'
                / 'developers.json'
            ),
            fs_write=self.fs_write,
        )
        return self.snapshot_data.developers

    def download_developers(self):
        for developer in self.snapshot_data.developers:
            try:
                write_file(
                    Developers(self.auth, self.org_name, developer).get_developer().text,
                    str(
                        Path(self.target_directory)
                        / self.org_name
                        / 'developers'
                        / (developer + '.json')
                    ),
                    fs_write=self.fs_write,
                )
            except HTTPError as e:
                console.echo(
                    f'Ignoring {type(e).__name__} {e.response.status_code} error for Developer ({developer})'
                )
            self._progress_callback(desc='Developers')
        return self.snapshot_data.developers

    def download_apiproducts_snapshot(self):
        self.snapshot_data.apiproducts = Apiproducts(
            self.auth, self.org_name, None
        ).list_api_products(prefix=self.prefix, format='dict')
        write_file(
            self.snapshot_data.apiproducts,
            str(
                Path(self.target_directory)
                / self.org_name
                / self.SNAPSHOTS_DIRECTORY_NAME
                / 'apiproducts'
                / 'apiproducts.json'
            ),
            fs_write=self.fs_write,
        )
        return self.snapshot_data.apiproducts

    def download_apiproducts(self):
        for apiproduct in self.snapshot_data.apiproducts:
            try:
                write_file(
                    Apiproducts(self.auth, self.org_name, apiproduct).get_api_product().text,
                    str(
                        Path(self.target_directory)
                        / self.org_name
                        / 'apiproducts'
                        / (apiproduct + '.json')
                    ),
                    fs_write=self.fs_write,
                )
            except HTTPError as e:
                console.echo(
                    f'Ignoring {type(e).__name__} {e.response.status_code} error for API Product ({apiproduct})'
                )
            self._progress_callback(desc='API Products')
        return self.snapshot_data.apiproducts

    def download_apps_snapshot(self, expand=False, count=1000, startkey=""):
        self.snapshot_data.apps = Apps(
            self.auth, self.org_name, None
        ).list_apps_for_all_developers(
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
                str(
                    Path(self.target_directory)
                    / self.org_name
                    / self.SNAPSHOTS_DIRECTORY_NAME
                    / 'apps'
                    / (app + '.json')
                ),
                fs_write=self.fs_write,
            )
        return self.snapshot_data.apps

    def download_apps(self):
        for developer, apps in self.snapshot_data.apps.items():
            for app in apps:
                try:
                    write_file(
                        Apps(self.auth, self.org_name, app)
                        .get_developer_app_details(developer)
                        .text,
                        str(
                            Path(self.target_directory)
                            / self.org_name
                            / 'apps'
                            / developer
                            / (app + '.json')
                        ),
                        fs_write=self.fs_write,
                    )
                except HTTPError as e:
                    console.echo(
                        f'Ignoring {type(e).__name__} {e.response.status_code} error for Developer App ({app})'
                    )
                self._progress_callback(desc='Developer Apps')
        return self.snapshot_data.apps

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
            str(
                Path(self.target_directory)
                / self.org_name
                / self.SNAPSHOTS_DIRECTORY_NAME
                / 'userroles'
                / 'userroles.json'
            ),
            fs_write=self.fs_write,
        )
        return self.snapshot_data.userroles

    def _get_users_for_a_role(self, role_name):
        return Userroles(self.auth, self.org_name, role_name).get_users_for_a_role().text

    def _get_permissions(self, role_name):
        return Permissions(self.auth, self.org_name, role_name).get_permissions(
            formatted=True, format='text'
        )

    def download_userroles(self):
        for userrole in self.snapshot_data.userroles:
            try:
                write_file(
                    self._get_users_for_a_role(userrole),
                    str(
                        Path(self.target_directory)
                        / self.org_name
                        / 'userroles'
                        / userrole
                        / 'users.json'
                    ),
                    fs_write=self.fs_write,
                )
            except HTTPError as e:
                console.echo(
                    f'Ignoring {type(e).__name__} {e.response.status_code} error for User Role ({userrole}) users'
                )
            try:
                write_file(
                    self._get_permissions(userrole),
                    str(
                        Path(self.target_directory)
                        / self.org_name
                        / 'userroles'
                        / userrole
                        / 'resource_permissions.json'
                    ),
                    fs_write=self.fs_write,
                )
            except HTTPError as e:
                console.echo(
                    f'Ignoring {type(e).__name__} {e.response.status_code} error for User Role ({userrole}) resource permissions'
                )
            self._progress_callback(desc='User Roles')
        return self.snapshot_data.userroles

    def _calculate_snapshot_size(self):
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
        if 'apis' in self.apis:
            console.echo(
                'Retrieving API Proxies listing (this may take a while)... ',
                end='',
                flush=True,
            )
            self.download_apis_snapshot()
            console.echo('Done')
        if 'keyvaluemaps' in self.apis:
            console.echo('Retrieving KeyValueMaps listing... ', end='', flush=True)
            self.download_keyvaluemaps_snapshot()
            console.echo('Done')
        if 'targetservers' in self.apis:
            console.echo('Retrieving TargetServers listing... ', end='', flush=True)
            self.download_targetservers_snapshot()
            console.echo('Done')
        if 'caches' in self.apis:
            console.echo('Retrieving Caches listing... ', end='', flush=True)
            self.download_caches_snapshot()
            console.echo('Done')
        if 'developers' in self.apis:
            console.echo('Retrieving Developers listing... ', end='', flush=True)
            self.download_developers_snapshot()
            console.echo('Done')
        if 'apiproducts' in self.apis:
            console.echo('Retrieving API Products listing... ', end='', flush=True)
            self.download_apiproducts_snapshot()
            console.echo('Done')
        if 'apps' in self.apis:
            console.echo(
                'Retrieving Developer Apps listing (this may take a while)... ',
                end='',
                flush=True,
            )
            self.download_apps_snapshot()
            console.echo('Done')
        if 'userroles' in self.apis:
            console.echo('Retrieving User Roles listing... ', end='', flush=True)
            self.download_userroles_snapshot()
            console.echo('Done')
        self.snapshot_size = self._calculate_snapshot_size()
        return self.snapshot_data

    def take_snapshot(self):
        self.get_snapshots()
        console.echo('Generating snapshot files...')
        if 'apis' in self.apis:
            self.download_apis()
        if 'keyvaluemaps' in self.apis:
            self.download_keyvaluemaps()
        if 'targetservers' in self.apis:
            self.download_targetservers()
        if 'caches' in self.apis:
            self.download_caches()
        if 'developers' in self.apis:
            self.download_developers()
        if 'apiproducts' in self.apis:
            self.download_apiproducts()
        if 'apps' in self.apis:
            self.download_apps()
        if 'userroles' in self.apis:
            self.download_userroles()
        self.progress_bar.close()
        console.echo('Done.')
        return self.snapshot_data
