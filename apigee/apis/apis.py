import json
import logging
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
                          paths_exist, run_func_on_dir_files,
                          run_func_on_iterable, split_path, write_zip)

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
        if len(args) == 4:
            InformalPullInterface.__init__(self, args[0], args[1], args[2], args[3], **kwargs)
        else:
            InformalApisInterface.__init__(self, args[0], args[1])

    def __get_and_export(self, resource_type, files, environment, dependencies=[], force=True):
        resource = getattr(self, f'get_{resource_type}_dependencies')(files)
        dependencies.extend(resource)
        getattr(self, f'export_{resource_type}_dependencies')(environment, resource, force=force)
        return dependencies

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

    def delete_undeployed_revisions(self, api_name, save_last=0, dry_run=False):
        details = ApisSerializer().filter_deployment_details(
            Deployments(self._auth, self._org_name, api_name)
            .get_api_proxy_deployment_details()
            .json()
        )
        undeployed = ApisSerializer().filter_undeployed_revisions(
            self.list_api_proxy_revisions(api_name).json(),
            ApisSerializer().filter_deployed_revisions(details),
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
            except Exception as e:
                logging.warning(f'{e}; file={f}', exc_info=True)

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
            except Exception as e:
                logging.warning(f'{e}; file={f}', exc_info=True)

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
            except Exception as e:
                logging.warning(f'{e}; file={f}', exc_info=True)

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
        for resource_type in ('keyvaluemap', 'targetserver', 'cache'):
            self._Apis__get_and_export(
                resource_type, files, self._environment, dependencies=dependencies, force=force
            )
        return export, dependencies
