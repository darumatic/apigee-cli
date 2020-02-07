#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import json
import os
import requests
import sys
import xml.etree.ElementTree as et
import zipfile
from pathlib import Path

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.apis import IApis, ApisSerializer, IPull
from apigee.api.deployments import Deployments
from apigee.api.keyvaluemaps import Keyvaluemaps
from apigee.api.targetservers import Targetservers
from apigee.util import authorization
from apigee.util.os import (makedirs, path_exists, paths_exist,
    extractzip, writezip, splitpath)

class Apis(IApis, IPull):

    def __init__(self, *args, **kwargs):
        IApis.__init__(self, args[0], args[1], args[2])#auth, org_name, api_name
        try:
            IPull.__init__(self, args[0], args[1], args[2], args[3], args[4], **kwargs)#auth, org_name, api_name, revision_number, environment, work_tree=None
        except IndexError as ie:
            pass

    def delete_api_proxy_revision(self, revision_number):
        uri = '{0}/v1/organizations/{1}/apis/{2}/revisions/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name,
                    revision_number)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def gen_deployment_detail(self, deployment):
        return {
            'name':deployment['name'],'revision':[
                revision['name'] for revision in deployment['revision']
            ]
        }

    def delete_revisions(self, revisions):
        for rev in revisions:
            print('Deleting revison', rev)
            self.delete_api_proxy_revision(rev)

    def delete_undeployed_revisions(self, save_last=0, dry_run=False):
        revisions = self.list_api_proxy_revisions().json()
        deployments = Deployments(self._auth, self._org_name, self._api_name)
        deployment_details = []
        deployed = []
        for dep in deployments.get_api_proxy_deployment_details().json()['environment']:
            deployment_details.append(self.gen_deployment_detail(dep))
        for dep in deployment_details:
            deployed.extend(dep['revision'])
        deployed = list(set(deployed))
        undeployed = [int(rev) for rev in revisions if rev not in deployed]
        undeployed.sort()
        undeployed_length = len(undeployed)
        undeployed = undeployed[:undeployed_length - (save_last if save_last <= undeployed_length else undeployed_length)]
        print('Undeployed revisions:', undeployed)
        if dry_run:
            return
        self.delete_revisions(undeployed)

    def export_api_proxy(self, revision_number, write=True, output_file=None):
        uri = '{0}/v1/organizations/{1}/apis/{2}/revisions/{3}?format=bundle' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name,
                    revision_number)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        if write:
            writezip(output_file, resp.content)
        return resp

    def get_api_proxy(self):
        uri = '{0}/v1/organizations/{1}/apis/{2}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_api_proxies(self, prefix=None):
        uri = '{0}/v1/organizations/{1}/apis' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return ApisSerializer().serialize_details(resp, 'json', prefix=prefix)

    def list_api_proxy_revisions(self):
        uri = '{0}/v1/organizations/{1}/apis/{2}/revisions' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
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

    def export_keyvaluemap_dependencies(self, environment, keyvaluemaps, force=False):
        makedirs(self._keyvaluemaps_dir)
        for keyvaluemap in keyvaluemaps:
            keyvaluemap_file = str(Path(self._keyvaluemaps_dir) / keyvaluemap)
            if not force:
                path_exists(keyvaluemap_file)
            print('Pulling', keyvaluemap, 'and writing to', os.path.abspath(keyvaluemap_file))
            resp = Keyvaluemaps(self._auth, self._org_name, keyvaluemap).get_keyvaluemap_in_an_environment(environment).text
            print(resp)
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

    def export_targetserver_dependencies(self, environment, targetservers, force=False):
        makedirs(self._targetservers_dir)
        for targetserver in targetservers:
            targetserver_file = str(Path(self._targetservers_dir) / targetserver)
            if not force:
                path_exists(targetserver_file)
            print('Pulling', targetserver, 'and writing to', os.path.abspath(targetserver_file))
            resp = Targetservers(self._auth, self._org_name, targetserver).get_targetserver(environment).text
            print(resp)
            with open(targetserver_file, 'w') as f:
                f.write(resp)

    def replace_substring(self, file, old, new):
        with open(file, 'r') as f:
            body = str()
            try:
                body = f.read()
            except Exception as e:
                print(type(e).__name__, e)
                print('Ignoring', file)
            if old in body:
                with open(file, 'w') as nf:
                    nf.write(body.replace(old, new))
                print('M  ', os.path.abspath(file))

    def prefix_dependencies_in_work_tree(self, dependencies, prefix):
        dependencies = [dep for dep in dependencies if not dep.startswith(prefix)]
        directory = self._work_tree
        files = []
        for filename in Path(directory).resolve().rglob('*'):
            if not filename.is_dir() and '.git' not in splitpath(str(filename)):
                files.append(str(filename))
        print('Prefixing', dependencies, 'with', prefix)
        for f in files:
            for dep in dependencies:
                self.replace_substring(f, dep, prefix+dep)

    def get_apiproxy_basepath(self, directory):
        default_file = str(Path(directory) / 'apiproxy/proxies/default.xml')
        tree = et.parse(default_file)
        try:
            return tree.find('.//BasePath').text, default_file
        except AttributeError as ae:
            sys.exit('No BasePath found in ' + default_file)

    def set_apiproxy_basepath(self, basepath, file):
        default_file = os.path.abspath(file)
        tree = et.parse(default_file)
        current_basepath = None
        try:
            current_basepath = tree.find('.//BasePath').text
        except AttributeError as ae:
            sys.exit('No BasePath found in ' + default_file)
        with open(default_file, 'r+') as f:
            body = f.read().replace(current_basepath, basepath)
            f.seek(0)
            f.write(body)
            f.truncate()
        print(current_basepath, '->', basepath)
        print('M  ', default_file)

    def pull(self, dependencies=[], force=False, prefix=None, basepath=None):
        apis = Apis(self._auth, self._org_name, self._api_name)
        dependencies.append(self._api_name)

        makedirs(self._work_tree)

        if not force:
            paths_exist([self._zip_file, self._apiproxy_dir])

        print('Writing ZIP to', os.path.abspath(self._zip_file))
        apis = apis.export_api_proxy(self._revision_number, write=True, output_file=self._zip_file)

        makedirs(self._apiproxy_dir)

        print('Extracting', self._zip_file, 'in', os.path.abspath(self._apiproxy_dir))
        extractzip(self._zip_file, self._apiproxy_dir)

        os.remove(self._zip_file)

        files = self.get_apiproxy_files(self._apiproxy_dir)

        keyvaluemaps = self.get_keyvaluemap_dependencies(files)

        print('KeyValueMap dependencies found:', keyvaluemaps)
        dependencies.extend(keyvaluemaps)

        self.export_keyvaluemap_dependencies(self._environment, keyvaluemaps, force=force)

        targetservers = self.get_targetserver_dependencies(files)

        print('TargetServer dependencies found:', targetservers)
        dependencies.extend(targetservers)

        self.export_targetserver_dependencies(self._environment, targetservers, force=force)

        if prefix:
            self.prefix_dependencies_in_work_tree(set(dependencies), prefix)

        if basepath:
            _, file = self.get_apiproxy_basepath(self._apiproxy_dir)
            self.set_apiproxy_basepath(basepath, file)

        return apis, keyvaluemaps, targetservers
