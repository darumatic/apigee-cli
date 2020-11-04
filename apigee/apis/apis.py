import json
import os
import sys
import xml.etree.ElementTree as et
from pathlib import Path

import requests

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.apis.interfaces.apis_interface import InformalApisInterface
from apigee.apis.interfaces.pull_interface import InformalPullInterface
from apigee.apis.serializer import ApisSerializer
from apigee.caches.caches import Caches
from apigee.deployments.deployments import Deployments
from apigee.keyvaluemaps.keyvaluemaps import Keyvaluemaps
from apigee.targetservers.targetservers import Targetservers
from apigee.utils import (extract_zip, is_dir, make_dirs, path_exists,
                          paths_exist, remove_last_items_from_list,
                          run_func_on_dir_files, run_func_on_iterable,
                          split_path, write_zip)

DELETE_API_PROXY_REVISION_PATH = (
    '{api_url}/v1/organizations/{org}/apis/{api_name}/revisions/{revision_number}'
)
DEPLOY_API_PROXY_REVISION_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/apis/{api_name}/revisions/{revision_number}/deployments?delay={delay}'
EXPORT_API_PROXY_PATH = (
    '{api_url}/v1/organizations/{org}/apis/{api_name}/revisions/{revision_number}?format=bundle'
)
GET_API_PROXY_PATH = '{api_url}/v1/organizations/{org}/apis/{api_name}'
LIST_API_PROXIES_PATH = '{api_url}/v1/organizations/{org}/apis'
LIST_API_PROXY_REVISIONS_PATH = '{api_url}/v1/organizations/{org}/apis/{api_name}/revisions'
UNDEPLOY_API_PROXY_REVISION_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/apis/{api_name}/revisions/{revision_number}/deployments'
FORCE_UNDEPLOY_API_PROXY_REVISION_PATH = '{api_url}/v1/organizations/{org}/apis/{api_name}/revisions/{revision_number}/deployments?action=undeploy&env={environment}&force=true'


class Apis(InformalApisInterface, InformalPullInterface):
    def __init__(self, *args, **kwargs):
        InformalApisInterface.__init__(self, args[0], args[1])
        try:
            InformalPullInterface.__init__(self, args[0], args[1], args[2], args[3], **kwargs)
        except IndexError:
            pass

    def delete_api_proxy_revision(self, api_name, revision_number):
        uri = DELETE_API_PROXY_REVISION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            api_name=api_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def deploy_api_proxy_revision(
        self, api_name, environment, revision_number, delay=0, override=False
    ):
        uri = DEPLOY_API_PROXY_REVISION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            api_name=api_name,
            revision_number=revision_number,
            delay=delay,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        )
        resp = requests.post(uri, headers=hdrs, data={'override': 'true' if override else 'false'})
        resp.raise_for_status()
        return resp

    @staticmethod
    def filter_deployment_details(details):
        return run_func_on_iterable(
            details['environment'],
            lambda d: {
                'name': d['name'],
                'revision': [revision['name'] for revision in d['revision']],
            },
        )

    @staticmethod
    def filter_deployed_revisions(details):
        return list(set(run_func_on_iterable(details, lambda d: d['revision'], state_op='extend')))

    @staticmethod
    def filter_undeployed_revisions(revisions, deployed, save_last=0):
        return remove_last_items_from_list(
            sorted([int(rev) for rev in revisions if rev not in deployed]), save_last
        )

    def delete_undeployed_revisions(self, api_name, save_last=0, dry_run=False):
        details = Apis.filter_deployment_details(
            Deployments(self._auth, self._org_name, api_name)
            .get_api_proxy_deployment_details()
            .json()
        )
        undeployed = Apis.filter_undeployed_revisions(
            self.list_api_proxy_revisions(api_name).json(),
            Apis.filter_deployed_revisions(details),
            save_last=save_last,
        )
        console.echo(f'Undeployed revisions to be deleted: {undeployed}')
        if dry_run:
            return undeployed

        def _func(revision):
            console.echo(f'Deleting revison {revision}')
            self.delete_api_proxy_revision(api_name, revision)

        return run_func_on_iterable(undeployed, _func)

    def export_api_proxy(self, api_name, revision_number, fs_write=True, output_file=None):
        uri = EXPORT_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            api_name=api_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        if fs_write:
            write_zip(output_file, resp.content)
        return resp

    def get_api_proxy(self, api_name):
        uri = GET_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, api_name=api_name
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_api_proxies(self, prefix=None, format='json'):
        uri = LIST_API_PROXIES_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name)
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return ApisSerializer().serialize_details(resp, format, prefix=prefix)

    def list_api_proxy_revisions(self, api_name):
        uri = LIST_API_PROXY_REVISIONS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, api_name=api_name
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def undeploy_api_proxy_revision(self, api_name, environment, revision_number):
        uri = UNDEPLOY_API_PROXY_REVISION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            api_name=api_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def force_undeploy_api_proxy_revision(self, api_name, environment, revision_number):
        uri = FORCE_UNDEPLOY_API_PROXY_REVISION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            api_name=api_name,
            revision_number=revision_number,
            environment=environment,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_apiproxy_files(self, directory):
        return run_func_on_dir_files(str(Path(directory) / 'apiproxy'), lambda f: f)

    def get_keyvaluemap_dependencies(self, files):
        def _func(f, _state):
            try:
                root = et.parse(f).getroot()
                if root.tag == 'KeyValueMapOperations':
                    if root.attrib['mapIdentifier'] not in _state:
                        _state.add(root.attrib['mapIdentifier'])
                        return root.attrib['mapIdentifier']
            except:
                pass

        return run_func_on_iterable(files, _func, args=(set(),))

    def export_keyvaluemap_dependencies(
        self, environment, keyvaluemaps, force=False, expc_verbosity=1
    ):
        make_dirs(self._keyvaluemaps_dir)

        def _func(kvm):
            kvm_file = str(Path(self._keyvaluemaps_dir) / kvm)
            if not force:
                path_exists(os.path.relpath(kvm_file))
            resp = (
                Keyvaluemaps(self._auth, self._org_name, kvm)
                .get_keyvaluemap_in_an_environment(environment)
                .text
            )
            console.echo(resp, expc_verbosity=1)
            with open(kvm_file, 'w') as f:
                f.write(resp)

        return run_func_on_iterable(keyvaluemaps, _func)

    def get_targetserver_dependencies(self, files):
        def _func(f, _state):
            try:
                root = et.parse(f).getroot()
                for child in root.iter('Server'):
                    if child.attrib['name'] not in _state:
                        _state.add(child.attrib['name'])
                        return child.attrib['name']
            except:
                pass

        return run_func_on_iterable(files, _func, args=(set(),))

    def export_targetserver_dependencies(
        self, environment, targetservers, force=False, expc_verbosity=1
    ):
        make_dirs(self._targetservers_dir)

        def _func(ts):
            ts_file = str(Path(self._targetservers_dir) / ts)
            if not force:
                path_exists(os.path.relpath(ts_file))
            resp = Targetservers(self._auth, self._org_name, ts).get_targetserver(environment).text
            console.echo(resp, expc_verbosity=1)
            with open(ts_file, 'w') as f:
                f.write(resp)

        return run_func_on_iterable(targetservers, _func)

    def get_cache_dependencies(self, files):
        def _func(f, _state):
            try:
                name = et.parse(f).find('.//CacheResource').text
                if name and name not in _state:
                    _state.add(name)
                    return name
            except:
                pass

        return run_func_on_iterable(files, _func, args=(set(),))

    def export_cache_dependencies(self, environment, caches, force=False, expc_verbosity=1):
        make_dirs(self._caches_dir)

        def _func(cache):
            cache_file = str(Path(self._caches_dir) / cache)
            if not force:
                path_exists(os.path.relpath(cache_file))
            resp = (
                Caches(self._auth, self._org_name, cache)
                .get_information_about_a_cache(environment)
                .text
            )
            console.echo(resp, expc_verbosity=1)
            with open(cache_file, 'w') as f:
                f.write(resp)

        return run_func_on_iterable(caches, _func)

    @staticmethod
    def replace_substring(file, old, new):
        with open(file, 'r') as f:
            body = ""
            try:
                body = f.read()
            except Exception as e:
                console.echo(type(e).__name__, e)
                console.echo(f'Ignoring {os.path.relpath(file)}')
            if old in body:
                with open(file, 'w') as nf:
                    nf.write(body.replace(old, new))
                console.echo(f'M  {os.path.relpath(file)}')

    def prefix_dependencies_in_work_tree(self, dependencies, prefix):
        dependencies = [d for d in dependencies if not d.startswith(prefix)]

        def _cond(file_path):
            return not is_dir(file_path) and '.git' not in split_path(file_path)

        def _func(file_path):
            if _cond(file_path):
                for d in dependencies:
                    Apis.replace_substring(file_path, d, prefix + d)

        return run_func_on_dir_files(self._work_tree, _func)

    def get_apiproxy_basepath(self, directory):
        default_file = str(Path(directory) / 'apiproxy/proxies/default.xml')
        tree = et.parse(default_file)
        try:
            return tree.find('.//BasePath').text, default_file
        except AttributeError:
            sys.exit(f'No BasePath found in {default_file}')

    def set_apiproxy_basepath(self, basepath, file):
        default_file = os.path.abspath(file)
        tree = et.parse(default_file)
        current_basepath = None
        try:
            current_basepath = tree.find('.//BasePath').text
        except AttributeError:
            sys.exit(f'No BasePath found in {default_file}')
        with open(default_file, 'r+') as f:
            body = f.read().replace(current_basepath, basepath)
            f.seek(0)
            f.write(body)
            f.truncate()
        console.echo(f'{current_basepath} -> {basepath}')
        console.echo(f'M  {os.path.relpath(default_file)}')

    def _get_and_export(self, resource_type, files, environment, dependencies=[], force=True):
        resource = getattr(self, f'get_{resource_type}_dependencies')(files)
        dependencies.extend(resource)
        getattr(self, f'export_{resource_type}_dependencies')(environment, resource, force=force)
        return dependencies

    def pull(self, api_name, dependencies=[], force=False, prefix=None, basepath=None):
        dependencies.append(api_name)
        make_dirs(self._work_tree)
        self.apiproxy_dir = api_name
        if not force:
            paths_exist((os.path.relpath(self._zip_file), os.path.relpath(self._apiproxy_dir)))
        export = self.export_api_proxy(
            api_name, self._revision_number, fs_write=True, output_file=self._zip_file
        )
        make_dirs(self._apiproxy_dir)
        extract_zip(self._zip_file, self._apiproxy_dir)
        os.remove(self._zip_file)
        files = self.get_apiproxy_files(self._apiproxy_dir)
        for resource_type in ['keyvaluemap', 'targetserver', 'cache']:
            self._get_and_export(
                resource_type, files, self._environment, dependencies=dependencies, force=force
            )
        if prefix:
            self.prefix_dependencies_in_work_tree(set(dependencies), prefix)
        if basepath:
            _, file = self.get_apiproxy_basepath(self._apiproxy_dir)
            self.set_apiproxy_basepath(basepath, file)
        return export, dependencies
