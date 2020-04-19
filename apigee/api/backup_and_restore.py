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
from apigee.util.os import touch, extractzip, isfile, isdir, read_file, write_file
from apigee.util.types import Struct


def list_proxies(auth, org, prefix=None):
    return json.loads(Apis(auth, org, None).list_api_proxies(prefix=prefix))


def get_proxy(auth, org, api_name):
    return Apis(auth, org, None).get_api_proxy(api_name)


def export_proxy(auth, org, api_name, revision_number, fs_write=True, output_file=None):
    return Apis(auth, org, None).export_api_proxy(
        api_name, revision_number, fs_write=fs_write, output_file=output_file
    )


def list_kvms(auth, org, environment, prefix=None):
    return json.loads(
        Keyvaluemaps(auth, org, None).list_keyvaluemaps_in_an_environment(
            environment, prefix=prefix
        )
    )


def get_kvm(auth, org, environment, kvm_name):
    return Keyvaluemaps(auth, org, kvm_name).get_keyvaluemap_in_an_environment(
        environment
    )


def list_targetservers(auth, org, environment, prefix=None):
    return json.loads(
        Targetservers(auth, org, None).list_targetservers_in_an_environment(
            environment, prefix=prefix
        )
    )


def get_targetserver(auth, org, environment, targetserver_name):
    return Targetservers(auth, org, targetserver_name).get_targetserver(environment)


def list_caches(auth, org, environment, prefix=None):
    return json.loads(
        Caches(auth, org, None).list_caches_in_an_environment(
            environment, prefix=prefix
        )
    )


def get_cache(auth, org, environment, cache_name):
    return Caches(auth, org, cache_name).get_information_about_a_cache(environment)


def list_developers(auth, org, prefix=None, expand=False, count=1000, startkey=""):
    return json.loads(
        Developers(auth, org, None).list_developers(
            prefix=prefix, expand=expand, count=count, startkey=startkey,
        )
    )


def get_developer(auth, org, developer_name):
    return Developers(auth, org, developer_name).get_developer()


def list_apps(auth, org, prefix=None, expand=False, count=1000, startkey=""):
    apps = {}
    apps_obj = Apps(auth, org, None)
    for dev in list_developers(
        auth, org, prefix=prefix, expand=expand, count=count, startkey=startkey,
    ):
        apps[dev] = json.loads(
            apps_obj.list_developer_apps(
                dev, prefix=None, expand=expand, count=1000, startkey=startkey
            )
        )
    return apps


def get_app(auth, org, developer_name, app_name):
    return Apps(auth, org, app_name).get_developer_app_details(developer_name)


def list_products(auth, org, prefix=None, expand=False, count=1000, startkey=""):
    return json.loads(
        Apiproducts(auth, org, None).list_api_products(
            prefix=None, expand=expand, count=1000, startkey=startkey
        )
    )


def get_product(auth, org, product_name):
    return Apiproducts(auth, org, product_name).get_api_product()


def list_roles(auth, org, prefix=None):
    return Userroles(auth, org, None).list_user_roles().json()


def get_users_for_role(auth, org, role_name):
    try:
        return Userroles(auth, org, role_name).get_users_for_a_role().text
    except HTTPError as e:
        return str(e)


def get_permissions(auth, org, role_name):
    try:
        return (
            Permissions(auth, org, role_name)
            .get_permissions(formatted=True, format="json")
            .text
        )
    except HTTPError as e:
        return str(e)


def snapshot_apis(
    auth,
    org,
    struct,
    environments=["test", "prod"],
    prefix=None,
    fs_write=False,
    base_dir="snapshots",
    apis_dir="apis",
):
    for api in list_proxies(auth, org, prefix=None):
        struct.apis[api] = get_proxy(auth, org, api).json()
        write_file(
            struct.apis[api],
            str(Path(org) / base_dir / apis_dir / (api + ".json")),
            fs_write=fs_write,
        )
    return struct


def snapshot_kvms(
    auth,
    org,
    struct,
    environment,
    prefix=None,
    fs_write=False,
    base_dir="snapshots",
    kvms_dir="keyvaluemaps",
):
    try:
        struct.kvms[environment] = list_kvms(auth, org, environment, prefix=prefix)
    except HTTPError:
        struct.kvms[environment] = []
    write_file(
        struct.kvms[environment],
        str(Path(org) / base_dir / kvms_dir / environment / "keyvaluemaps.json"),
        fs_write=fs_write,
    )
    return struct


def snapshot_targetservers(
    auth,
    org,
    struct,
    environment,
    prefix=None,
    fs_write=False,
    base_dir="snapshots",
    targetservers_dir="targetservers",
):
    try:
        struct.targetservers[environment] = list_targetservers(
            auth, org, environment, prefix=prefix
        )
    except HTTPError:
        struct.targetservers[environment] = []
    write_file(
        struct.targetservers[environment],
        str(
            Path(org)
            / base_dir
            / targetservers_dir
            / environment
            / "targetservers.json"
        ),
        fs_write=fs_write,
    )
    return struct


def snapshot_caches(
    auth,
    org,
    struct,
    environment,
    prefix=None,
    fs_write=False,
    base_dir="snapshots",
    caches_dir="caches",
):
    try:
        struct.caches[environment] = list_caches(auth, org, environment, prefix=prefix)
    except HTTPError:
        struct.caches[environment] = []
    write_file(
        struct.caches[environment],
        str(Path(org) / base_dir / caches_dir / environment / "caches.json"),
        fs_write=fs_write,
    )
    return struct


def snapshot_developers(
    auth,
    org,
    struct,
    prefix=None,
    fs_write=False,
    base_dir="snapshots",
    developers_dir="developers",
):
    struct.developers = list_developers(auth, org, prefix=None)
    write_file(
        struct.developers,
        str(Path(org) / base_dir / developers_dir / "developers.json"),
        fs_write=fs_write,
    )
    return struct


def snapshot_products(
    auth,
    org,
    struct,
    prefix=None,
    fs_write=False,
    base_dir="snapshots",
    products_dir="apiproducts",
):
    struct.products = list_products(auth, org, prefix=None)
    write_file(
        struct.products,
        str(Path(org) / base_dir / products_dir / "apiproducts.json"),
        fs_write=fs_write,
    )
    return struct


def snapshot_apps(
    auth,
    org,
    struct,
    prefix=None,
    fs_write=False,
    base_dir="snapshots",
    apps_dir="apps",
):
    struct.apps = list_apps(auth, org, prefix=None)
    for k, v in struct.apps.items():
        write_file(
            v, str(Path(org) / base_dir / apps_dir / (k + ".json")), fs_write=fs_write,
        )
    return struct


def snapshot_roles(
    auth,
    org,
    struct,
    prefix=None,
    fs_write=False,
    base_dir="snapshots",
    roles_dir="userroles",
):
    struct.roles = list_roles(auth, org, prefix=None)
    write_file(
        struct.roles,
        str(Path(org) / base_dir / roles_dir / "userroles.json"),
        fs_write=fs_write,
    )
    return struct


def snapshot(
    auth,
    org,
    environments=["test", "prod"],
    prefix=None,
    fs_write=False,
    base_dir="snapshots",
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
    snapshot_apis(
        auth, org, struct, environments=environments, prefix=prefix, fs_write=fs_write,
    )
    for env in environments:
        snapshot_kvms(
            auth, org, struct, environment=env, prefix=prefix, fs_write=fs_write,
        )
        snapshot_targetservers(
            auth, org, struct, environment=env, prefix=prefix, fs_write=fs_write,
        )
        snapshot_caches(
            auth, org, struct, environment=env, prefix=prefix, fs_write=fs_write,
        )
    snapshot_developers(
        auth, org, struct, prefix=prefix, fs_write=fs_write,
    )
    snapshot_products(
        auth, org, struct, prefix=prefix, fs_write=fs_write,
    )
    snapshot_apps(
        auth, org, struct, prefix=prefix, fs_write=fs_write,
    )
    snapshot_roles(
        auth, org, struct, prefix=prefix, fs_write=fs_write,
    )
    return struct


def backup_apis(auth, org, snapshot, prefix=None, fs_write=True, apis_dir="apis"):
    for api, metadata in snapshot.apis.items():
        for rev in metadata["revision"]:
            output_dir = str(Path(org) / apis_dir / api / rev)
            output_zip = str(Path(output_dir) / (api + ".zip"))
            touch(output_zip)
            export_proxy(auth, org, api, rev, fs_write=fs_write, output_file=output_zip)
            extractzip(output_zip, output_dir)
            os.remove(output_zip)
    return snapshot


def backup_kvms(
    auth,
    org,
    snapshot,
    environment,
    prefix=None,
    fs_write=True,
    kvms_dir="keyvaluemaps",
):
    for kvm in snapshot.kvms[environment]:
        write_file(
            get_kvm(auth, org, environment, kvm).text,
            str(Path(org) / kvms_dir / environment / (kvm + ".json")),
            fs_write=fs_write,
        )
    return snapshot


def backup_targetservers(
    auth,
    org,
    snapshot,
    environment,
    prefix=None,
    fs_write=True,
    targetservers_dir="targetservers",
):
    for targetserver in snapshot.targetservers[environment]:
        write_file(
            get_targetserver(auth, org, environment, targetserver).text,
            str(Path(org) / targetservers_dir / environment / (targetserver + ".json")),
            fs_write=fs_write,
        )
    return snapshot


def backup_caches(
    auth, org, snapshot, environment, prefix=None, fs_write=True, caches_dir="caches",
):
    for cache in snapshot.caches[environment]:
        write_file(
            get_cache(auth, org, environment, cache).text,
            str(Path(org) / caches_dir / environment / (cache + ".json")),
            fs_write=fs_write,
        )
    return snapshot


def backup_developers(
    auth, org, snapshot, prefix=None, fs_write=True, developers_dir="developers"
):
    for dev in snapshot.developers:
        write_file(
            get_developer(auth, org, dev).text,
            str(Path(org) / developers_dir / (dev + ".json")),
            fs_write=fs_write,
        )
    return snapshot


def backup_products(
    auth, org, snapshot, prefix=None, fs_write=True, products_dir="apiproducts"
):
    for product in snapshot.products:
        write_file(
            get_product(auth, org, product).text,
            str(Path(org) / products_dir / (product + ".json")),
            fs_write=fs_write,
        )
    return snapshot


def backup_apps(auth, org, snapshot, prefix=None, fs_write=True, apps_dir="apps"):
    for dev, apps in snapshot.apps.items():
        for app in apps:
            write_file(
                get_app(auth, org, dev, app).text,
                str(Path(org) / apps_dir / dev / (app + ".json")),
                fs_write=fs_write,
            )
    return snapshot


def backup_roles(
    auth, org, snapshot, prefix=None, fs_write=True, roles_dir="userroles"
):
    for role in snapshot.roles:
        write_file(
            get_users_for_role(auth, org, role),
            str(Path(org) / roles_dir / role / "users.json"),
            fs_write=fs_write,
        )
        write_file(
            get_permissions(auth, org, role),
            str(Path(org) / roles_dir / role / "resource_permissions.json"),
            fs_write=fs_write,
        )
    return snapshot


def backup(
    auth, org, environments=["test", "prod"], prefix=None, fs_write=True,
):
    curr_snapshot = snapshot(
        auth, org, environments=environments, prefix=prefix, fs_write=fs_write,
    )
    backup_apis(
        auth, org, curr_snapshot, prefix=prefix, fs_write=fs_write,
    )
    for env in environments:
        backup_kvms(
            auth, org, curr_snapshot, env, prefix=prefix, fs_write=fs_write,
        )
        backup_targetservers(
            auth, org, curr_snapshot, env, prefix=prefix, fs_write=fs_write,
        )
        backup_caches(
            auth, org, curr_snapshot, env, prefix=prefix, fs_write=fs_write,
        )
    backup_developers(auth, org, curr_snapshot, prefix=prefix, fs_write=fs_write)
    backup_products(auth, org, curr_snapshot, prefix=prefix, fs_write=fs_write)
    backup_apps(auth, org, curr_snapshot, prefix=prefix, fs_write=fs_write)
    backup_roles(auth, org, curr_snapshot, prefix=prefix, fs_write=fs_write)


def restore_kvms(auth, org, environment, directory, snapshot=[], dry_run=False):
    if not snapshot:
        return
    missing = []
    curr_snapshot = list_kvms(auth, org, environment)
    for kvm_file in os.listdir(directory):
        path = str(Path(directory) / kvm_file)
        kvm_name = read_file(path, type="json")["name"]
        if kvm_name in snapshot and kvm_name not in curr_snapshot:
            if not dry_run:
                Keyvaluemaps(auth, org, None).push_keyvaluemap(environment, path)
            missing.append(kvm_name)
    console.log(
        f"Missing key value maps that will be restored: {json.dumps(missing)}",
        silent=not dry_run,
    )
    return missing


def restore_targetservers(
    auth, org, environment, directory, snapshot=[], dry_run=False
):
    if not snapshot:
        return
    missing = []
    curr_snapshot = list_targetservers(auth, org, environment)
    for targetserver_file in os.listdir(directory):
        path = str(Path(directory) / targetserver_file)
        targetserver_name = read_file(path, type="json")["name"]
        if targetserver_name in snapshot and targetserver_name not in curr_snapshot:
            if not dry_run:
                Targetservers(auth, org, None).push_targetserver(environment, path)
            missing.append(targetserver_name)
    console.log(
        f"Missing target servers that will be restored: {json.dumps(missing)}",
        silent=not dry_run,
    )
    return missing


def restore_caches(auth, org, environment, directory, snapshot=[], dry_run=False):
    if not snapshot:
        return
    missing = []
    curr_snapshot = list_caches(auth, org, environment)
    for cache_file in os.listdir(directory):
        path = str(Path(directory) / cache_file)
        cache_name = read_file(path, type="json")["name"]
        if cache_name in snapshot and cache_name not in curr_snapshot:
            if not dry_run:
                Caches(auth, org, None).push_cache(environment, path)
            missing.append(cache_name)
    console.log(
        f"Missing caches that will be restored: {json.dumps(missing)}",
        silent=not dry_run,
    )
    return missing


def restore_developers(auth, org, directory, snapshot=[], dry_run=False):
    if not snapshot:
        return
    missing = []
    curr_snapshot = list_developers(auth, org)
    for developer_file in os.listdir(directory):
        path = str(Path(directory) / developer_file)
        developer_name = read_file(path, type="json")["email"]
        if developer_name in snapshot and developer_name not in curr_snapshot:
            if not dry_run:
                content = read_file(path, type="json")
                Developers(auth, org, content["email"]).create_developer(
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


def restore_products(auth, org, directory, snapshot=[], dry_run=False):
    if not snapshot:
        return
    missing = []
    curr_snapshot = list_products(auth, org)
    for product_file in os.listdir(directory):
        path = str(Path(directory) / product_file)
        product_name = read_file(path, type="json")["name"]
        if product_name in snapshot and product_name not in curr_snapshot:
            if not dry_run:
                Apiproducts(auth, org, None).push_apiproducts(path)
            missing.append(product_name)
    console.log(
        f"Missing API products that will be restored: {json.dumps(missing)}",
        silent=not dry_run,
    )
    return missing


def restore_apps(auth, org, directory, snapshot_dir, dry_run=False):
    missing = {}
    curr_snapshot = list_apps(auth, org)
    pathlist = Path(directory).glob("**/*")
    for app_file in pathlist:
        if isfile(app_file):
            app_name = read_file(app_file, type="json")["name"]
            developer_name = os.path.split(os.path.split(app_file)[0])[1]
            try:
                snapshot = read_file(
                    str(Path(snapshot_dir) / (developer_name + ".json")), type="json",
                )
            except FileNotFoundError:
                snapshot = read_file(
                    str(Path(snapshot_dir) / developer_name), type="json"
                )
            try:
                curr_snapshot[developer_name]
            except KeyError:
                curr_snapshot[developer_name] = []
            if app_name in snapshot and app_name not in curr_snapshot[developer_name]:
                if not dry_run:
                    content = read_file(app_file, type="json")
                    content["developerId"] = developer_name
                    write_file(content, app_file)
                    Apps(auth, org, None).restore_app(app_file)
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


def restore_permissions(auth, org, role_name, file):
    return Permissions(auth, org, role_name).create_permissions(
        json.dumps(read_file(file, type="json"))
    )


def restore_users(auth, org, role_name, file):
    users = read_file(file, type="json")
    for user in users:
        Userroles(auth, org, role_name).add_a_user_to_a_role(user)
    return get_users_for_role(auth, org, role_name)


def restore_roles(auth, org, directory, snapshot=[], dry_run=False):
    if not snapshot:
        return
    missing = []
    curr_snapshot = list_roles(auth, org)
    pathlist = Path(directory).glob("**/*")
    for role_path in pathlist:
        if isdir(role_path):
            role_name = os.path.split(role_path)[1]
            if role_name in snapshot and role_name not in curr_snapshot:
                if not dry_run:
                    Userroles(
                        auth, org, [role_name]
                    ).create_a_user_role_in_an_organization()
                    if isfile(str(Path(role_path) / "resource_permissions.json")):
                        restore_permissions(
                            auth,
                            org,
                            role_name,
                            str(Path(role_path) / "resource_permissions.json"),
                        )
                    if isfile(str(Path(role_path) / "users.json")):
                        restore_users(
                            auth, org, role_name, str(Path(role_path) / "users.json"),
                        )
                missing.append(role_name)
    console.log(
        f"Missing user roles that will be restored: {json.dumps(missing)}",
        silent=not dry_run,
    )
    return missing
