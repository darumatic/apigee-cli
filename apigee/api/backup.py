#!/usr/bin/env python3

import json
import os
from pathlib import Path
from requests.exceptions import HTTPError

from apigee.api.apis import Apis
from apigee.api.keyvaluemaps import Keyvaluemaps
from apigee.api.targetservers import Targetservers
from apigee.api.caches import Caches
from apigee.api.developers import Developers
from apigee.api.apps import Apps
from apigee.api.apiproducts import Apiproducts
from apigee.api.permissions import Permissions
from apigee.api.userroles import Userroles

# from apigee.util import authorization, console
from apigee.util.os import touch, extractzip, write_file
from apigee.util.types import Struct


class Backup:
    def __init__(
        self, auth, org_name, target_directory=None, snapshots_dir="snapshots"
    ):
        self._auth = auth
        self._org_name = org_name
        self._snapshots_dir = snapshots_dir
        if target_directory:
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)
            self._target_directory = str(Path(target_directory).resolve())
        else:
            self._target_directory = os.getcwd()

    @property
    def auth(self):
        return self._auth

    @auth.setter
    def auth(self, value):
        self._auth = value

    @property
    def org_name(self):
        return self._org_name

    @org_name.setter
    def org_name(self, value):
        self._org_name = value

    @property
    def target_directory(self):
        return self._target_directory

    @target_directory.setter
    def target_directory(self, value):
        self._target_directory = str(Path(value).resolve())

    @property
    def snapshots_dir(self):
        return self._snapshots_dir

    @snapshots_dir.setter
    def snapshots_dir(self, value):
        self._snapshots_dir = value

    def _get_users_for_a_role(self, role_name):
        try:
            return (
                Userroles(self._auth, self._org_name, role_name)
                .get_users_for_a_role()
                .text
            )
        except HTTPError as e:
            return str(e)

    def _get_permissions(self, role_name):
        try:
            return Permissions(self._auth, self._org_name, role_name).get_permissions(
                formatted=True, format="text"
            )
        except HTTPError as e:
            return str(e)

    def snapshot_apis(
        self, struct, prefix=None, fs_write=False,
    ):
        for api in Apis(self._auth, self._org_name, None).list_api_proxies(
            prefix=prefix, format="dict"
        ):
            struct.apis[api] = (
                Apis(self._auth, self._org_name, None).get_api_proxy(api).json()
            )
            write_file(
                struct.apis[api],
                str(
                    Path(self._target_directory)
                    / self._org_name
                    / self._snapshots_dir
                    / "apis"
                    / (api + ".json")
                ),
                fs_write=fs_write,
            )
        return struct

    def snapshot_kvms(
        self, struct, environment, prefix=None, fs_write=False,
    ):
        try:
            struct.kvms[environment] = Keyvaluemaps(
                self._auth, self._org_name, None
            ).list_keyvaluemaps_in_an_environment(
                environment, prefix=prefix, format="dict"
            )
        except HTTPError:
            struct.kvms[environment] = []
        write_file(
            struct.kvms[environment],
            str(
                Path(self._target_directory)
                / self._org_name
                / self._snapshots_dir
                / "keyvaluemaps"
                / environment
                / "keyvaluemaps.json"
            ),
            fs_write=fs_write,
        )
        return struct

    def snapshot_targetservers(
        self, struct, environment, prefix=None, fs_write=False,
    ):
        try:
            struct.targetservers[environment] = Targetservers(
                self._auth, self._org_name, None
            ).list_targetservers_in_an_environment(
                environment, prefix=prefix, format="dict"
            )
        except HTTPError:
            struct.targetservers[environment] = []
        write_file(
            struct.targetservers[environment],
            str(
                Path(self._target_directory)
                / self._org_name
                / self._snapshots_dir
                / "targetservers"
                / environment
                / "targetservers.json"
            ),
            fs_write=fs_write,
        )
        return struct

    def snapshot_caches(
        self, struct, environment, prefix=None, fs_write=False,
    ):
        try:
            struct.caches[environment] = Caches(
                self._auth, self._org_name, None
            ).list_caches_in_an_environment(environment, prefix=prefix, format="dict")
        except HTTPError:
            struct.caches[environment] = []
        write_file(
            struct.caches[environment],
            str(
                Path(self._target_directory)
                / self._org_name
                / self._snapshots_dir
                / "caches"
                / environment
                / "caches.json"
            ),
            fs_write=fs_write,
        )
        return struct

    def snapshot_developers(
        self, struct, prefix=None, fs_write=False,
    ):
        struct.developers = Developers(
            self._auth, self._org_name, None
        ).list_developers(prefix=prefix, format="dict")
        write_file(
            struct.developers,
            str(
                Path(self._target_directory)
                / self._org_name
                / self._snapshots_dir
                / "developers"
                / "developers.json"
            ),
            fs_write=fs_write,
        )
        return struct

    def snapshot_products(
        self, struct, prefix=None, fs_write=False,
    ):
        struct.products = Apiproducts(
            self._auth, self._org_name, None
        ).list_api_products(prefix=prefix, format="dict")
        write_file(
            struct.products,
            str(
                Path(self._target_directory)
                / self._org_name
                / self._snapshots_dir
                / "apiproducts"
                / "apiproducts.json"
            ),
            fs_write=fs_write,
        )
        return struct

    def snapshot_apps(
        self, struct, prefix=None, fs_write=False,
    ):
        struct.apps = Apps(
            self._auth, self._org_name, None
        ).list_apps_for_all_developers(prefix=prefix, format="dict")
        for k, v in struct.apps.items():
            write_file(
                v,
                str(
                    Path(self._target_directory)
                    / self._org_name
                    / self._snapshots_dir
                    / "apps"
                    / (k + ".json")
                ),
                fs_write=fs_write,
            )
        return struct

    def snapshot_roles(
        self, struct, prefix=None, fs_write=False,
    ):
        struct.roles = (
            Userroles(self._auth, self._org_name, None).list_user_roles().json()
        )
        write_file(
            struct.roles,
            str(
                Path(self._target_directory)
                / self._org_name
                / self._snapshots_dir
                / "userroles"
                / "userroles.json"
            ),
            fs_write=fs_write,
        )
        return struct

    def snapshot(
        self, environments=["test", "prod"], prefix=None, fs_write=False, resources=None
    ):
        struct = Struct(
            apis={},
            kvms={},
            targetservers={},
            caches={},
            developers=[],
            apps={},
            products=[],
            roles=[],
        )
        if not resources:
            self.snapshot_apis(
                struct, prefix=prefix, fs_write=fs_write,
            )
            for env in environments:
                self.snapshot_kvms(
                    struct, environment=env, prefix=prefix, fs_write=fs_write,
                )
                self.snapshot_targetservers(
                    struct, environment=env, prefix=prefix, fs_write=fs_write,
                )
                self.snapshot_caches(
                    struct, environment=env, prefix=prefix, fs_write=fs_write,
                )
            self.snapshot_developers(
                struct, prefix=prefix, fs_write=fs_write,
            )
            self.snapshot_products(
                struct, prefix=prefix, fs_write=fs_write,
            )
            self.snapshot_apps(
                struct, prefix=prefix, fs_write=fs_write,
            )
            self.snapshot_roles(
                struct, prefix=prefix, fs_write=fs_write,
            )
            return struct
        for resource in resources:
            if resource == "apis":
                self.snapshot_apis(
                    struct, prefix=prefix, fs_write=fs_write,
                )
            elif resource == "keyvaluemaps":
                for env in environments:
                    self.snapshot_kvms(
                        struct, environment=env, prefix=prefix, fs_write=fs_write,
                    )
            elif resource == "targetservers":
                for env in environments:
                    self.snapshot_targetservers(
                        struct, environment=env, prefix=prefix, fs_write=fs_write,
                    )
            elif resource == "caches":
                for env in environments:
                    self.snapshot_caches(
                        struct, environment=env, prefix=prefix, fs_write=fs_write,
                    )
            elif resource == "developers":
                self.snapshot_developers(
                    struct, prefix=prefix, fs_write=fs_write,
                )
            elif resource == "apiproducts":
                self.snapshot_products(
                    struct, prefix=prefix, fs_write=fs_write,
                )
            elif resource == "apps":
                self.snapshot_apps(
                    struct, prefix=prefix, fs_write=fs_write,
                )
            elif resource == "userroles":
                self.snapshot_roles(
                    struct, prefix=prefix, fs_write=fs_write,
                )
        return struct

    def backup_apis(self, snapshot, prefix=None, fs_write=True):
        for api, metadata in snapshot.apis.items():
            for rev in metadata["revision"]:
                output_dir = str(
                    Path(self._target_directory) / self._org_name / "apis" / api / rev
                )
                output_zip = str(Path(output_dir) / (api + ".zip"))
                touch(output_zip)
                Apis(self._auth, self._org_name, None).export_api_proxy(
                    api, rev, fs_write=fs_write, output_file=output_zip
                )
                extractzip(output_zip, output_dir)
                os.remove(output_zip)
        return snapshot

    def backup_kvms(
        self, snapshot, environment, prefix=None, fs_write=True,
    ):
        for kvm in snapshot.kvms[environment]:
            write_file(
                Keyvaluemaps(self._auth, self._org_name, kvm)
                .get_keyvaluemap_in_an_environment(environment)
                .text,
                str(
                    Path(self._target_directory)
                    / self._org_name
                    / "keyvaluemaps"
                    / environment
                    / (kvm + ".json")
                ),
                fs_write=fs_write,
            )
        return snapshot

    def backup_targetservers(
        self, snapshot, environment, prefix=None, fs_write=True,
    ):
        for targetserver in snapshot.targetservers[environment]:
            write_file(
                Targetservers(self._auth, self._org_name, targetserver)
                .get_targetserver(environment)
                .text,
                str(
                    Path(self._target_directory)
                    / self._org_name
                    / "targetservers"
                    / environment
                    / (targetserver + ".json")
                ),
                fs_write=fs_write,
            )
        return snapshot

    def backup_caches(
        self, snapshot, environment, prefix=None, fs_write=True,
    ):
        for cache in snapshot.caches[environment]:
            write_file(
                Caches(self._auth, self._org_name, cache)
                .get_information_about_a_cache(environment)
                .text,
                str(
                    Path(self._target_directory)
                    / self._org_name
                    / "caches"
                    / environment
                    / (cache + ".json")
                ),
                fs_write=fs_write,
            )
        return snapshot

    def backup_developers(self, snapshot, prefix=None, fs_write=True):
        for dev in snapshot.developers:
            write_file(
                Developers(self._auth, self._org_name, dev).get_developer().text,
                str(
                    Path(self._target_directory)
                    / self._org_name
                    / "developers"
                    / (dev + ".json")
                ),
                fs_write=fs_write,
            )
        return snapshot

    def backup_products(self, snapshot, prefix=None, fs_write=True):
        for product in snapshot.products:
            write_file(
                Apiproducts(self._auth, self._org_name, product).get_api_product().text,
                str(
                    Path(self._target_directory)
                    / self._org_name
                    / "apiproducts"
                    / (product + ".json")
                ),
                fs_write=fs_write,
            )
        return snapshot

    def backup_apps(self, snapshot, prefix=None, fs_write=True):
        for dev, apps in snapshot.apps.items():
            for app in apps:
                write_file(
                    Apps(self._auth, self._org_name, app)
                    .get_developer_app_details(dev)
                    .text,
                    str(
                        Path(self._target_directory)
                        / self._org_name
                        / "apps"
                        / dev
                        / (app + ".json")
                    ),
                    fs_write=fs_write,
                )
        return snapshot

    def backup_roles(self, snapshot, prefix=None, fs_write=True):
        for role in snapshot.roles:
            write_file(
                self._get_users_for_a_role(role),
                str(
                    Path(self._target_directory)
                    / self._org_name
                    / "userroles"
                    / role
                    / "users.json"
                ),
                fs_write=fs_write,
            )
            write_file(
                self._get_permissions(role),
                str(
                    Path(self._target_directory)
                    / self._org_name
                    / "userroles"
                    / role
                    / "resource_permissions.json"
                ),
                fs_write=fs_write,
            )
        return snapshot

    def backup(
        self, environments=["test", "prod"], prefix=None, fs_write=True, resources=None
    ):
        curr_snapshot = self.snapshot(
            environments=environments, prefix=prefix, fs_write=fs_write, resources=resources
        )
        if not resources:
            self.backup_apis(
                curr_snapshot, prefix=prefix, fs_write=fs_write,
            )
            for env in environments:
                self.backup_kvms(
                    curr_snapshot, env, prefix=prefix, fs_write=fs_write,
                )
                self.backup_targetservers(
                    curr_snapshot, env, prefix=prefix, fs_write=fs_write,
                )
                self.backup_caches(
                    curr_snapshot, env, prefix=prefix, fs_write=fs_write,
                )
            self.backup_developers(curr_snapshot, prefix=prefix, fs_write=fs_write)
            self.backup_products(curr_snapshot, prefix=prefix, fs_write=fs_write)
            self.backup_apps(curr_snapshot, prefix=prefix, fs_write=fs_write)
            self.backup_roles(curr_snapshot, prefix=prefix, fs_write=fs_write)
            return
        for resource in resources:
            if resource == "apis":
                self.backup_apis(
                    curr_snapshot, prefix=prefix, fs_write=fs_write,
                )
            elif resource == "keyvaluemaps":
                for env in environments:
                    self.backup_kvms(
                        curr_snapshot, env, prefix=prefix, fs_write=fs_write,
                    )
            elif resource == "targetservers":
                for env in environments:
                    self.backup_targetservers(
                        curr_snapshot, env, prefix=prefix, fs_write=fs_write,
                    )
            elif resource == "caches":
                for env in environments:
                    self.backup_caches(
                        curr_snapshot, env, prefix=prefix, fs_write=fs_write,
                    )
            elif resource == "developers":
                self.backup_developers(curr_snapshot, prefix=prefix, fs_write=fs_write)
            elif resource == "apiproducts":
                self.backup_products(curr_snapshot, prefix=prefix, fs_write=fs_write)
            elif resource == "apps":
                self.backup_apps(curr_snapshot, prefix=prefix, fs_write=fs_write)
            elif resource == "userroles":
                self.backup_roles(curr_snapshot, prefix=prefix, fs_write=fs_write)
