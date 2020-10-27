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
from apigee.types import APIS, Struct, empty_snapshot
from apigee.userroles.userroles import Userroles
from apigee.utils import (extract_zip, resolve_target_directory, touch,
                          write_file)


class Backups:

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
        self.apis = sorted(apis)
        self.environments = environments
        self.snapshot_data = empty_snapshot()
        self.snapshot_size = 0
        self.progress_bar = None
        self.org_path = Path(self.target_directory) / self.org_name

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
            if t not in APIS:
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

    def _gen_snapshot_path(self, subpaths=[]):
        path = self.org_path / self.SNAPSHOTS_DIRECTORY_NAME
        for subpath in subpaths:
            path /= subpath
        return str(path)

    def _gen_download_path(self, subpaths=[]):
        path = self.org_path
        for subpath in subpaths:
            path /= subpath
        return str(path)

    def download_apis_snapshot(self):
        for api in Apis(self.auth, self.org_name, None).list_api_proxies(
            prefix=self.prefix, format='dict'
        ):
            self.snapshot_data.apis[api] = (
                Apis(self.auth, self.org_name, None).get_api_proxy(api).json()
            )
            data = {
                'snapshot': self.snapshot_data.apis[api],
                'target_path': self._gen_snapshot_path(subpaths=['apis', f'{api}.json']),
                'fs_write': self.fs_write,
                'indent': 2,
            }
            write_file(
                data['snapshot'],
                data['target_path'],
                fs_write=data['fs_write'],
                indent=data['indent'],
            )
        return self.snapshot_data.apis

    def download_apis(self):
        for api, metadata in self.snapshot_data.apis.items():
            for revision in metadata['revision']:
                output_file = self._gen_download_path(
                    subpaths=['apis', api, revision, f'{api}.zip']
                )
                target_directory = os.path.dirname(output_file)
                try:
                    Apis(self.auth, self.org_name, None).export_api_proxy(
                        api, revision, fs_write=True, output_file=output_file
                    )
                    extract_zip(output_file, target_directory)
                    os.remove(output_file)
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
            data = {
                'snapshot': self.snapshot_data.keyvaluemaps[environment],
                'target_path': self._gen_snapshot_path(
                    subpaths=['keyvaluemaps', environment, 'keyvaluemaps.json']
                ),
                'fs_write': self.fs_write,
                'indent': 2,
            }
            write_file(
                data['snapshot'],
                data['target_path'],
                fs_write=data['fs_write'],
                indent=data['indent'],
            )
        return self.snapshot_data.keyvaluemaps

    def download_keyvaluemaps(self):
        for environment in self.environments:
            for kvm in self.snapshot_data.keyvaluemaps[environment]:
                try:
                    data = {
                        'snapshot': Keyvaluemaps(self.auth, self.org_name, kvm)
                        .get_keyvaluemap_in_an_environment(environment)
                        .text,
                        'target_path': self._gen_download_path(
                            subpaths=['keyvaluemaps', environment, f'{kvm}.json']
                        ),
                        'fs_write': self.fs_write,
                    }
                    write_file(data['snapshot'], data['target_path'], fs_write=data['fs_write'])
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
            data = {
                'snapshot': self.snapshot_data.targetservers[environment],
                'target_path': self._gen_snapshot_path(
                    subpaths=['targetservers', environment, 'targetservers.json']
                ),
                'fs_write': self.fs_write,
                'indent': 2,
            }
            write_file(
                data['snapshot'],
                data['target_path'],
                fs_write=data['fs_write'],
                indent=data['indent'],
            )
        return self.snapshot_data.targetservers

    def download_targetservers(self):
        for environment in self.environments:
            for targetserver in self.snapshot_data.targetservers[environment]:
                try:
                    data = {
                        'snapshot': Targetservers(self.auth, self.org_name, targetserver)
                        .get_targetserver(environment)
                        .text,
                        'target_path': self._gen_download_path(
                            subpaths=['targetservers', environment, f'{targetserver}.json']
                        ),
                        'fs_write': self.fs_write,
                    }
                    write_file(data['snapshot'], data['target_path'], fs_write=data['fs_write'])
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
            data = {
                'snapshot': self.snapshot_data.caches[environment],
                'target_path': self._gen_snapshot_path(
                    subpaths=['caches', environment, 'caches.json']
                ),
                'fs_write': self.fs_write,
                'indent': 2,
            }
            write_file(
                data['snapshot'],
                data['target_path'],
                fs_write=data['fs_write'],
                indent=data['indent'],
            )
        return self.snapshot_data.caches

    def download_caches(self):
        for environment in self.environments:
            for cache in self.snapshot_data.caches[environment]:
                try:
                    data = {
                        'snapshot': Caches(self.auth, self.org_name, cache)
                        .get_information_about_a_cache(environment)
                        .text,
                        'target_path': self._gen_download_path(
                            subpaths=['caches', environment, f'{cache}.json']
                        ),
                        'fs_write': self.fs_write,
                    }
                    write_file(data['snapshot'], data['target_path'], fs_write=data['fs_write'])
                except HTTPError as e:
                    console.echo(
                        f'Ignoring {type(e).__name__} {e.response.status_code} error for Cache ({cache})'
                    )
                self._progress_callback(desc='Caches')
        return self.snapshot_data.caches

    def download_developers_snapshot(self):
        self.snapshot_data.developers = Developers(self.auth, self.org_name, None).list_developers(
            prefix=self.prefix, format='dict'
        )
        data = {
            'snapshot': self.snapshot_data.developers,
            'target_path': self._gen_snapshot_path(subpaths=['developers', 'developers.json']),
            'fs_write': self.fs_write,
            'indent': 2,
        }
        write_file(
            data['snapshot'], data['target_path'], fs_write=data['fs_write'], indent=data['indent']
        )
        return self.snapshot_data.developers

    def download_developers(self):
        for developer in self.snapshot_data.developers:
            try:
                data = {
                    'snapshot': Developers(self.auth, self.org_name, developer)
                    .get_developer()
                    .text,
                    'target_path': self._gen_download_path(
                        subpaths=['developers', f'{developer}.json']
                    ),
                    'fs_write': self.fs_write,
                }
                write_file(data['snapshot'], data['target_path'], fs_write=data['fs_write'])
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
        data = {
            'snapshot': self.snapshot_data.apiproducts,
            'target_path': self._gen_snapshot_path(subpaths=['apiproducts', 'apiproducts.json']),
            'fs_write': self.fs_write,
            'indent': 2,
        }
        write_file(
            data['snapshot'], data['target_path'], fs_write=data['fs_write'], indent=data['indent']
        )
        return self.snapshot_data.apiproducts

    def download_apiproducts(self):
        for apiproduct in self.snapshot_data.apiproducts:
            try:
                data = {
                    'snapshot': Apiproducts(self.auth, self.org_name, apiproduct)
                    .get_api_product()
                    .text,
                    'target_path': self._gen_download_path(
                        subpaths=['apiproducts', f'{apiproduct}.json']
                    ),
                    'fs_write': self.fs_write,
                }
                write_file(data['snapshot'], data['target_path'], fs_write=data['fs_write'])
            except HTTPError as e:
                console.echo(
                    f'Ignoring {type(e).__name__} {e.response.status_code} error for API Product ({apiproduct})'
                )
            self._progress_callback(desc='API Products')
        return self.snapshot_data.apiproducts

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
            data = {
                'snapshot': details,
                'target_path': self._gen_snapshot_path(subpaths=['apps', f'{app}.json']),
                'fs_write': self.fs_write,
                'indent': 2,
            }
            write_file(
                data['snapshot'],
                data['target_path'],
                fs_write=data['fs_write'],
                indent=data['indent'],
            )
        return self.snapshot_data.apps

    def download_apps(self):
        for developer, apps in self.snapshot_data.apps.items():
            for app in apps:
                try:
                    data = {
                        'snapshot': Apps(self.auth, self.org_name, app)
                        .get_developer_app_details(developer)
                        .text,
                        'target_path': self._gen_download_path(
                            subpaths=['apps', developer, f'{app}.json']
                        ),
                        'fs_write': self.fs_write,
                    }
                    write_file(data['snapshot'], data['target_path'], fs_write=data['fs_write'])
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
        data = {
            'snapshot': self.snapshot_data.userroles,
            'target_path': self._gen_snapshot_path(subpaths=['userroles', 'userroles.json']),
            'fs_write': self.fs_write,
            'indent': 2,
        }
        write_file(
            data['snapshot'], data['target_path'], fs_write=data['fs_write'], indent=data['indent']
        )
        return self.snapshot_data.userroles

    def _get_users_for_a_role(self, role_name):
        return Userroles(self.auth, self.org_name, role_name).get_users_for_a_role().json()

    @staticmethod
    def _sort_lists_in_permissions(resource_permissions):
        for i in range(len(resource_permissions.get('resourcePermission'))):
            resource_permissions['resourcePermission'][i]['permissions'].sort()
        return resource_permissions

    def _get_permissions(self, role_name):
        return json.dumps(
            Backups._sort_lists_in_permissions(
                Permissions(self.auth, self.org_name, role_name).get_permissions(
                    formatted=True, format='json'
                )
            ),
            indent=2,
        )

    def _download_users_for_a_role(self, role_name):
        try:
            data = {
                'snapshot': self._get_users_for_a_role(role_name),
                'target_path': self._gen_download_path(
                    subpaths=['userroles', role_name, 'users.json']
                ),
                'fs_write': self.fs_write,
                'indent': 2,
            }
            write_file(
                data['snapshot'],
                data['target_path'],
                fs_write=data['fs_write'],
                indent=data['indent'],
            )
        except HTTPError as e:
            console.echo(
                f'Ignoring {type(e).__name__} {e.response.status_code} error for User Role ({role_name}) users'
            )

    def _download_resource_permissions(self, role_name):
        try:
            data = {
                'snapshot': self._get_permissions(role_name),
                'target_path': self._gen_download_path(
                    subpaths=['userroles', role_name, 'resource_permissions.json']
                ),
                'fs_write': self.fs_write,
            }
            write_file(data['snapshot'], data['target_path'], fs_write=data['fs_write'])
        except HTTPError as e:
            console.echo(
                f'Ignoring {type(e).__name__} {e.response.status_code} error for User Role ({role_name}) resource permissions'
            )

    def download_userroles(self):
        for role_name in self.snapshot_data.userroles:
            self._download_users_for_a_role(role_name)
            self._download_resource_permissions(role_name)
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
        for api in self.apis:
            if api in {'apis', 'apps'}:
                console.echo(
                    f'Retrieving {api} listing (this may take a while)... ', end='', flush=True
                )
            else:
                console.echo(f'Retrieving {api} listing... ', end='', flush=True)
            getattr(self, f'download_{api}_snapshot')()
            console.echo('Done')
        self.snapshot_size = self._calculate_snapshot_size()
        return self.snapshot_data

    def take_snapshot(self):
        self.get_snapshots()
        console.echo('Generating snapshot files...')
        for api in self.apis:
            getattr(self, f'download_{api}')()
        self.progress_bar.close()
        console.echo('Done.')
        return self.snapshot_data
