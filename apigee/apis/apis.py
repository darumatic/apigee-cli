import json
import os
import sys
import xml.etree.ElementTree as et
from pathlib import Path

import requests

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.caches.caches import Caches
from apigee.deployments.deployments import Deployments
from apigee.keyvaluemaps.keyvaluemaps import Keyvaluemaps
from apigee.targetservers.targetservers import Targetservers
from apigee.utils import (extract_zip, make_dirs, path_exists, paths_exist,
                          split_path, write_zip)

DELETE_API_PROXY_REVISION_PATH = (
    '{api_url}/v1/organizations/{org}/apis/{api_name}/revisions/{revision_number}'
)
DEPLOY_API_PROXY_REVISION_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/apis/{api_name}/revisions/{revision_number}/deployments?delay={delay}'
EXPORT_API_PROXY_PATH = '{api_url}/v1/organizations/{org}/apis/{api_name}/revisions/{revision_number}?format=bundle'
GET_API_PROXY_PATH = '{api_url}/v1/organizations/{org}/apis/{api_name}'
LIST_API_PROXIES_PATH = '{api_url}/v1/organizations/{org}/apis'
LIST_API_PROXY_REVISIONS_PATH = '{api_url}/v1/organizations/{org}/apis/{api_name}/revisions'
UNDEPLOY_API_PROXY_REVISION_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/apis/{api_name}/revisions/{revision_number}/deployments'
FORCE_UNDEPLOY_API_PROXY_REVISION_PATH = '{api_url}/v1/organizations/{org}/apis/{api_name}/revisions/{revision_number}/deployments?action=undeploy&env={environment}&force=true'


class ApisSerializer:
    def serialize_details(self, apis, format, prefix=None):
        resp = apis
        if format == 'text':
            return apis.text
        apis = apis.json()
        if prefix:
            apis = [api for api in apis if api.startswith(prefix)]
        if format == 'json':
            return json.dumps(apis)
        elif format == 'table':
            pass
        elif format == 'dict':
            return apis
        # else:
        #     raise ValueError(format)
        return resp


class IApis:
    def __init__(self, auth, org_name):
        self._auth = auth
        self._org_name = org_name

    def __call__(self):
        pass

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


class IPull:
    def __init__(self, auth, org_name, revision_number, environment, work_tree=None):
        self._auth = auth
        self._org_name = org_name
        if work_tree:
            if not os.path.exists(work_tree):
                os.makedirs(work_tree)
            self._work_tree = str(Path(work_tree).resolve())
        else:
            self._work_tree = os.getcwd()
        self._revision_number = revision_number
        self._environment = environment
        self._keyvaluemaps_dir = str(Path(self._work_tree) / 'keyvaluemaps' / environment)
        self._targetservers_dir = str(Path(self._work_tree) / 'targetservers' / environment)
        self._caches_dir = str(Path(self._work_tree) / 'caches' / environment)
        # self._apiproxy_dir = str(Path(self._work_tree) / api_name)
        self._apiproxy_dir = str(Path(self._work_tree))
        self._zip_file = str(Path(self._apiproxy_dir).with_suffix('.zip'))

    def __call__(self, *args, **kwargs):
        self.pull(*args, **kwargs)

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
    def revision_number(self):
        return self._revision_number

    @revision_number.setter
    def revision_number(self, value):
        self._revision_number = value

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        self._environment = value

    # @property
    # def work_tree(self):
    #     return self._work_tree
    #
    # @work_tree.setter
    # def work_tree(self, value):
    #     self.__init__(self._args, self._api_name, self._revision_number, work_tree=value)

    @property
    def keyvaluemaps_dir(self):
        return self._keyvaluemaps_dir

    @keyvaluemaps_dir.setter
    def keyvaluemaps_dir(self, value):
        self._keyvaluemaps_dir = str(Path(self._work_tree) / value / environment)

    @property
    def targetservers_dir(self):
        return self._targetservers_dir

    @targetservers_dir.setter
    def targetservers_dir(self, value):
        self._targetservers_dir = str(Path(self._work_tree) / value / environment)

    @property
    def caches_dir(self):
        return self._caches_dir

    @caches_dir.setter
    def caches_dir(self, value):
        self._caches_dir = str(Path(self._work_tree) / value / environment)

    @property
    def apiproxy_dir(self):
        return self._apiproxy_dir

    @apiproxy_dir.setter
    def apiproxy_dir(self, value):
        self._apiproxy_dir = str(Path(self._work_tree) / value)

    @property
    def zip_file(self):
        return self._zip_file

    @zip_file.setter
    def zip_file(self, value):
        self._zip_file = str(Path(self._apiproxy_dir) / value)


class Apis(IApis, IPull):
    def __init__(self, *args, **kwargs):
        IApis.__init__(self, args[0], args[1])  # auth, org_name
        try:
            IPull.__init__(
                self, args[0], args[1], args[2], args[3], **kwargs
            )  # auth, org_name, revision_number, environment, work_tree=None
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
        resp = requests.post(
            uri, headers=hdrs, data={'override': 'true' if override else 'false'}
        )
        resp.raise_for_status()
        return resp

    def gen_deployment_detail(self, deployment):
        return {
            'name': deployment['name'],
            'revision': [revision['name'] for revision in deployment['revision']],
        }

    def get_deployment_details(self, details):
        deployment_details = []
        for dep in details['environment']:
            deployment_details.append(self.gen_deployment_detail(dep))
        return deployment_details

    def get_deployed_revisions(self, details):
        deployed = []
        for dep in details:
            deployed.extend(dep['revision'])
        deployed = list(set(deployed))
        return deployed

    def get_undeployed_revisions(self, revisions, deployed, save_last=0):
        undeployed = sorted([int(rev) for rev in revisions if rev not in deployed])
        return undeployed[: -save_last if save_last > 0 else len(undeployed)]

    def delete_undeployed_revisions(self, api_name, save_last=0, dry_run=False):
        details = self.get_deployment_details(
            Deployments(self._auth, self._org_name, api_name)
            .get_api_proxy_deployment_details()
            .json()
        )
        undeployed = self.get_undeployed_revisions(
            self.list_api_proxy_revisions(api_name).json(),
            self.get_deployed_revisions(details),
            save_last=save_last,
        )
        console.echo(f'Undeployed revisions to be deleted: {undeployed}')
        if dry_run:
            return undeployed
        for rev in undeployed:
            console.echo(f'Deleting revison {rev}')
            self.delete_api_proxy_revision(api_name, rev)
        return undeployed

    def export_api_proxy(
        # self, api_name, revision_number, fs_write=True, write=True, output_file=None
        self,
        api_name,
        revision_number,
        fs_write=True,
        output_file=None,
    ):
        uri = EXPORT_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            api_name=api_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # if fs_write and write:
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
        files = []
        directory = str(Path(directory) / 'apiproxy')
        for filename in Path(directory).resolve().rglob('*'):
            files.append(str(filename))
        return files

    def get_keyvaluemap_dependencies(self, files):
        keyvaluemaps = []
        for f in files:
            try:
                root = et.parse(f).getroot()
                if root.tag == 'KeyValueMapOperations':
                    if root.attrib['mapIdentifier'] not in keyvaluemaps:
                        keyvaluemaps.append(root.attrib['mapIdentifier'])
            except:
                pass
        return keyvaluemaps

    def export_keyvaluemap_dependencies(
        self, environment, keyvaluemaps, force=False, expc_verbosity=1
    ):
        make_dirs(self._keyvaluemaps_dir)
        for keyvaluemap in keyvaluemaps:
            keyvaluemap_file = str(Path(self._keyvaluemaps_dir) / keyvaluemap)
            if not force:
                path_exists(os.path.relpath(keyvaluemap_file))
            resp = (
                Keyvaluemaps(self._auth, self._org_name, keyvaluemap)
                .get_keyvaluemap_in_an_environment(environment)
                .text
            )
            console.echo(resp, expc_verbosity=1)
            with open(keyvaluemap_file, 'w') as f:
                f.write(resp)

    def get_targetserver_dependencies(self, files):
        targetservers = []
        for f in files:
            try:
                root = et.parse(f).getroot()
                for child in root.iter('Server'):
                    if child.attrib['name'] not in targetservers:
                        targetservers.append(child.attrib['name'])
            except:
                pass
        return targetservers

    def export_targetserver_dependencies(
        self, environment, targetservers, force=False, expc_verbosity=1
    ):
        make_dirs(self._targetservers_dir)
        for targetserver in targetservers:
            targetserver_file = str(Path(self._targetservers_dir) / targetserver)
            if not force:
                path_exists(os.path.relpath(targetserver_file))
            resp = (
                Targetservers(self._auth, self._org_name, targetserver)
                .get_targetserver(environment)
                .text
            )
            console.echo(resp, expc_verbosity=1)
            with open(targetserver_file, 'w') as f:
                f.write(resp)

    def get_cache_dependencies(self, files):
        caches = []
        for f in files:
            try:
                name = et.parse(f).find('.//CacheResource').text
                if name and name not in caches:
                    caches.append(name)
            except:
                pass
        return caches

    def export_cache_dependencies(self, environment, caches, force=False, expc_verbosity=1):
        make_dirs(self._caches_dir)
        for cache in caches:
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

    def replace_substring(self, file, old, new):
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
        dependencies = [dep for dep in dependencies if not dep.startswith(prefix)]
        directory = self._work_tree
        files = []
        for filename in Path(directory).resolve().rglob('*'):
            if not filename.is_dir() and '.git' not in split_path(str(filename)):
                files.append(str(filename))
        for f in files:
            for dep in dependencies:
                self.replace_substring(f, dep, prefix + dep)

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

        keyvaluemaps = self.get_keyvaluemap_dependencies(files)
        dependencies.extend(keyvaluemaps)
        self.export_keyvaluemap_dependencies(self._environment, keyvaluemaps, force=force)

        targetservers = self.get_targetserver_dependencies(files)
        dependencies.extend(targetservers)
        self.export_targetserver_dependencies(self._environment, targetservers, force=force)

        caches = self.get_cache_dependencies(files)
        dependencies.extend(caches)
        self.export_cache_dependencies(self._environment, caches, force=force)

        if prefix:
            self.prefix_dependencies_in_work_tree(set(dependencies), prefix)

        if basepath:
            _, file = self.get_apiproxy_basepath(self._apiproxy_dir)
            self.set_apiproxy_basepath(basepath, file)

        return (export, keyvaluemaps, targetservers, caches)
