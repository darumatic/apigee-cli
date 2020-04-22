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

from apigee.util import authorization, console
from apigee.util.os import isfile, isdir, read_file, write_file


class Restore:
    def __init__(self, auth, org_name):
        self._auth = auth
        self._org_name = org_name

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

    def _get_users_for_a_role(self, role_name):
        try:
            return (
                Userroles(self._auth, self._org_name, role_name)
                .get_users_for_a_role()
                .text
            )
        except HTTPError as e:
            return str(e)

    def restore_kvms(self, environment, directory, snapshot=[], dry_run=False):
        if not snapshot:
            return
        missing = []
        curr_snapshot = Keyvaluemaps(
            self._auth, self._org_name, None
        ).list_keyvaluemaps_in_an_environment(environment, format="dict")
        for kvm_file in os.listdir(directory):
            path = str(Path(directory) / kvm_file)
            kvm_name = read_file(path, type="json")["name"]
            if kvm_name in snapshot and kvm_name not in curr_snapshot:
                if not dry_run:
                    Keyvaluemaps(self._auth, self._org_name, None).push_keyvaluemap(
                        environment, path
                    )
                missing.append(kvm_name)
        console.log(
            f"Missing key value maps that will be restored: {json.dumps(missing)}",
            silent=not dry_run,
        )
        return missing

    def restore_targetservers(self, environment, directory, snapshot=[], dry_run=False):
        if not snapshot:
            return
        missing = []
        curr_snapshot = Targetservers(
            self._auth, self._org_name, None
        ).list_targetservers_in_an_environment(environment, format="dict")
        for targetserver_file in os.listdir(directory):
            path = str(Path(directory) / targetserver_file)
            targetserver_name = read_file(path, type="json")["name"]
            if targetserver_name in snapshot and targetserver_name not in curr_snapshot:
                if not dry_run:
                    Targetservers(self._auth, self._org_name, None).push_targetserver(
                        environment, path
                    )
                missing.append(targetserver_name)
        console.log(
            f"Missing target servers that will be restored: {json.dumps(missing)}",
            silent=not dry_run,
        )
        return missing

    def restore_caches(self, environment, directory, snapshot=[], dry_run=False):
        if not snapshot:
            return
        missing = []
        curr_snapshot = Caches(
            self._auth, self._org_name, None
        ).list_caches_in_an_environment(environment, format="dict")
        for cache_file in os.listdir(directory):
            path = str(Path(directory) / cache_file)
            cache_name = read_file(path, type="json")["name"]
            if cache_name in snapshot and cache_name not in curr_snapshot:
                if not dry_run:
                    Caches(self._auth, self._org_name, None).push_cache(
                        environment, path
                    )
                missing.append(cache_name)
        console.log(
            f"Missing caches that will be restored: {json.dumps(missing)}",
            silent=not dry_run,
        )
        return missing

    def restore_developers(self, directory, snapshot=[], dry_run=False):
        if not snapshot:
            return
        missing = []
        curr_snapshot = Developers(self._auth, self._org_name, None).list_developers(
            format="dict"
        )
        for developer_file in os.listdir(directory):
            path = str(Path(directory) / developer_file)
            developer_name = read_file(path, type="json")["email"]
            if developer_name in snapshot and developer_name not in curr_snapshot:
                if not dry_run:
                    content = read_file(path, type="json")
                    Developers(
                        self._auth, self._org_name, content["email"]
                    ).create_developer(
                        content["firstName"],
                        content["lastName"],
                        content["userName"],
                        attributes=json.dumps({"attributes": content["attributes"]}),
                    )
                missing.append(developer_name)
        console.log(
            f"Missing developers that will be restored: {json.dumps(missing)}",
            silent=not dry_run,
        )
        return missing

    def restore_products(self, directory, snapshot=[], dry_run=False):
        if not snapshot:
            return
        missing = []
        curr_snapshot = Apiproducts(self._auth, self._org_name, None).list_api_products(
            format="dict"
        )
        for product_file in os.listdir(directory):
            path = str(Path(directory) / product_file)
            product_name = read_file(path, type="json")["name"]
            if product_name in snapshot and product_name not in curr_snapshot:
                if not dry_run:
                    Apiproducts(self._auth, self._org_name, None).push_apiproducts(path)
                missing.append(product_name)
        console.log(
            f"Missing API products that will be restored: {json.dumps(missing)}",
            silent=not dry_run,
        )
        return missing

    def restore_apps(self, directory, snapshot_dir, dry_run=False):
        missing = {}
        curr_snapshot = Apps(
            self._auth, self._org_name, None
        ).list_apps_for_all_developers(format="dict")
        pathlist = Path(directory).glob("**/*")
        for app_file in pathlist:
            if isfile(app_file):
                app_name = read_file(app_file, type="json")["name"]
                developer_name = os.path.split(os.path.split(app_file)[0])[1]
                try:
                    snapshot = read_file(
                        str(Path(snapshot_dir) / (developer_name + ".json")),
                        type="json",
                    )
                except FileNotFoundError:
                    snapshot = read_file(
                        str(Path(snapshot_dir) / developer_name), type="json"
                    )
                try:
                    curr_snapshot[developer_name]
                except KeyError:
                    curr_snapshot[developer_name] = []
                if (
                    app_name in snapshot
                    and app_name not in curr_snapshot[developer_name]
                ):
                    if not dry_run:
                        content = read_file(app_file, type="json")
                        content["developerId"] = developer_name
                        write_file(content, app_file)
                        Apps(self._auth, self._org_name, None).restore_app(app_file)
                    try:
                        missing[developer_name].append(app_name)
                    except KeyError:
                        missing[developer_name] = []
                        missing[developer_name].append(app_name)
        console.log(
            f"Missing developer apps that will be restored: {json.dumps(missing)}",
            silent=not dry_run,
        )
        return missing

    def restore_permissions(self, role_name, file):
        return Permissions(self._auth, self._org_name, role_name).create_permissions(
            json.dumps(read_file(file, type="json"))
        )

    def restore_users(self, role_name, file):
        users = read_file(file, type="json")
        for user in users:
            Userroles(self._auth, self._org_name, role_name).add_a_user_to_a_role(user)
        return self._get_users_for_a_role(role_name)

    def restore_roles(self, directory, snapshot=[], dry_run=False):
        if not snapshot:
            return
        missing = []
        curr_snapshot = (
            Userroles(self._auth, self._org_name, None).list_user_roles().json()
        )
        pathlist = Path(directory).glob("**/*")
        for role_path in pathlist:
            if isdir(role_path):
                role_name = os.path.split(role_path)[1]
                if role_name in snapshot and role_name not in curr_snapshot:
                    if not dry_run:
                        Userroles(
                            self._auth, self._org_name, [role_name]
                        ).create_a_user_role_in_an_organization()
                        if isfile(str(Path(role_path) / "resource_permissions.json")):
                            self.restore_permissions(
                                role_name,
                                str(Path(role_path) / "resource_permissions.json"),
                            )
                        if isfile(str(Path(role_path) / "users.json")):
                            self.restore_users(
                                role_name, str(Path(role_path) / "users.json"),
                            )
                    missing.append(role_name)
        console.log(
            f"Missing user roles that will be restored: {json.dumps(missing)}",
            silent=not dry_run,
        )
        return missing
