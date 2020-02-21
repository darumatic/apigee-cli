#!/usr/bin/env python
"""Source: https://apidocs.apigee.com/api-reference/content/api-proxies

The proxy APIs let you perform operations on API proxies, such as create, delete, update, and deploy.

You expose APIs on Apigee Edge by implementing API proxies. API proxies decouple the app-facing API from your backend services, shielding those apps from backend code changes. As you make backend changes to your services, apps continue to call the same API without any interruption.
"""

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
from apigee.util.os import makedirs
from apigee.util.os import path_exists
from apigee.util.os import paths_exist
from apigee.util.os import extractzip
from apigee.util.os import writezip
from apigee.util.os import splitpath

class Apis(IApis, IPull):

    def __init__(self, *args, **kwargs):
        """Apis constructor

        This constructor accepts a minimum of three positional arguments to initialize the IApis constructor,
        and a minimum of five positional arguments to initialize the IPull constructor.

        Args:
            auth: Apigee Edge credentials object.
            org_name: Apigee Edge organization.
            api_name: API Proxy name.
            revision_number: API Proxy revison to ``pull`` from Apigee.
            environment: Apigee environment.
            work_tree (optional): Target working directory. Defaults to None.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        IApis.__init__(self, args[0], args[1], args[2])#auth, org_name, api_name
        try:
            IPull.__init__(self, args[0], args[1], args[2], args[3], args[4], **kwargs)#auth, org_name, api_name, revision_number, environment, work_tree=None
        except IndexError as ie:
            pass

    def delete_api_proxy_revision(self, revision_number):
        """Deletes a revision of an API proxy and all policies, resources, endpoints, and revisions associated with it.

        The API proxy revision must be undeployed before you can delete it.

        Args:
            revision_number (int): The API proxy revision to delete.

        Returns:
            requests.Response()
        """
        uri = f'{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/apis/{self._api_name}/revisions/{revision_number}'
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def gen_deployment_detail(self, deployment):
        """Generates deployment detail

        Args:
            deployment (dict):

        Returns:
            dict
        """
        return {
            'name':deployment['name'],'revision':[
                revision['name'] for revision in deployment['revision']
            ]
        }

    def get_deployment_details(self, details):
        """Gets deployment details

        Args:
            details (dict):

        Returns:
            dict
        """
        deployment_details = []
        for dep in details['environment']:
            deployment_details.append(self.gen_deployment_detail(dep))
        return deployment_details

    def get_deployed_revisions(self, details):
        """Gets list of deployed revisions from deployment details.

        Args:
            details (dict):

        Returns:
            list
        """
        deployed = []
        for dep in details:
            deployed.extend(dep['revision'])
        deployed = list(set(deployed))
        return deployed

    def get_undeployed_revisions(self, revisions, deployed, save_last=0):
        """Gets list of undeployed revisions by comparing all API Proxy revisions with currently deployed revisons.

        Args:
            revisions (list): List of all API Proxy revisions.
            deployed (list): List of currently deployed API Proxy revisions.
            save_last (int, optional): Exclude ``n`` last revisions from result. Defaults to 0.

        Returns:
            list
        """
        undeployed = [int(rev) for rev in revisions if rev not in deployed]
        undeployed.sort()
        if save_last:
            return undeployed[:-save_last if save_last >= 0 else len(deployed)]
        return undeployed

    def delete_undeployed_revisions(self, save_last=0, dry_run=False):
        """Deletes all undeployed revisions of an API proxy and all policies, resources, and endpoints associated with it.

        Args:
            save_last (int, optional): Exclude ``n`` last revisions from deletion. Defaults to 0 (delete all undeployed revisions).
            dry_run (bool, optional): If True, only show revisions to be deleted (do not actually delete). Defaults to False.

        Returns:
            dict: list of revisions deleted or to be deleted (if ``dry_run`` is True).
        """
        deployed = self.get_deployed_revisions(self.get_deployment_details(Deployments(self._auth, self._org_name, self._api_name).get_api_proxy_deployment_details().json()))
        undeployed = self.get_undeployed_revisions(self.list_api_proxy_revisions().json(), deployed, save_last=save_last)
        print('Undeployed revisions to be deleted:', undeployed)
        if dry_run:
            return undeployed
        for rev in undeployed:
            print('Deleting revison', rev)
            self.delete_api_proxy_revision(rev)
        return undeployed

    def export_api_proxy(self, revision_number, write=True, output_file=None):
        """Outputs an API proxy revision as a ZIP formatted bundle of code and config files.

        This enables local configuration and development, including attachment of policies and scripts.

        Args:
            revision_number (int): The API Proxy revision to export.
            write (bool, optional): If True, write to ZIP file. Defaults to True.
            output_file (str, optional): Path of the output file. Defaults to None.

        Returns:
            requests.Response()
        """
        uri = f'{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/apis/{self._api_name}/revisions/{revision_number}?format=bundle'
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        if write:
            writezip(output_file, resp.content)
        return resp

    def get_api_proxy(self):
        """Gets an API proxy by name, including a list of existing revisions of the proxy.

        Args:
            None

        Returns:
            requests.Response()
        """
        uri = f'{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/apis/{self._api_name}'
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_api_proxies(self, prefix=None):
        """Gets the names of all API proxies in an organization.

        The names correspond to the names defined in the configuration files for each API proxy.

        Args:
            prefix (str, optional): Path of the output file.

        Returns:
            requests.Response()
        """
        uri = f'{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/apis'
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return ApisSerializer().serialize_details(resp, 'json', prefix=prefix)

    def list_api_proxy_revisions(self):
        """List all revisions for an API proxy.

        Args:
            None

        Returns:
            requests.Response()
        """
        uri = f'{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/apis/{self._api_name}/revisions'
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_apiproxy_files(self, directory):
        """Gets the paths of all ``apiproxy`` bundle files.

        Args:
            directory (str): Path of ``apiproxy`` bundle.

        Returns:
            list: list of ``apiproxy`` bundle files.
        """
        files = []
        directory = str(Path(directory) / 'apiproxy')
        for filename in Path(directory).resolve().rglob('*'):
            files.append(str(filename))
        return files

    def get_keyvaluemap_dependencies(self, files):
        """Gets all ``mapIdentifier`` names for all ``KeyValueMapOperations`` XML files.

        This will automatically ignore files that are not ``KeyValueMapOperations`` files.

        Args:
            files (list): List of ``KeyValueMapOperations`` XML files.

        Returns:
            list
        """
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
        """Exports KeyValueMaps from Apigee.

        Args:
            environment (str): Apigee environment.
            keyvaluemaps (list): List of KVMs to GET from Apigee.
            force (bool, optional): If True, overwrite existing files in the current working directory.
                Defaults to False.

        Returns:
            None
        """
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
        """Gets all ``Server`` values used in an API Proxy.

        Args:
            files (list): List of API Proxy files.

        Returns:
            list
        """
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
        """Exports Targetservers from Apigee.

        Args:
            environment (str): Apigee environment.
            targetservers (list): List of target servers to GET from Apigee.
            force (bool, optional): If True, overwrite existing files in the current working directory.
                Defaults to False.

        Returns:
            None
        """
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
        """Replaces old string in file with new string.

        Args:
            file (str): The file path.
            old (str): The old string to replace.
            new (str): The new string to replace the old string.

        Returns:
            None
        """
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
        """Adds a prefix string to all instances of the specified strings within the current working directory (recursively).

        This will ignore paths with ``.git``.

        Args:
            dependencies (list): List of strings to add a prefix to.
            prefix (str): Prefix to add.

        Returns:
            None
        """
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
        """Gets the basepath of an API Proxy by parsing an ``apiproxy`` bundle directory.

        Args:
            directory (str): Path of ``apiproxy`` bundle.

        Returns:
            str, str: basepath, file

        Raises:
            AttributeError: If no ``BasePath`` can be found.
        """
        default_file = str(Path(directory) / 'apiproxy/proxies/default.xml')
        tree = et.parse(default_file)
        try:
            return tree.find('.//BasePath').text, default_file
        except AttributeError as ae:
            sys.exit(f'No BasePath found in {default_file}')

    def set_apiproxy_basepath(self, basepath, file):
        """Sets the basepath of an API Proxy file.

        Args:
            basepath (str): New basepath to overwrite the existing one.
            file (str): Path of the file with the ``BasePath``.

        Returns:
            None

        Raises:
            AttributeError: If no ``BasePath`` can be found.
        """
        default_file = os.path.abspath(file)
        tree = et.parse(default_file)
        current_basepath = None
        try:
            current_basepath = tree.find('.//BasePath').text
        except AttributeError as ae:
            sys.exit(f'No BasePath found in {default_file}')
        with open(default_file, 'r+') as f:
            body = f.read().replace(current_basepath, basepath)
            f.seek(0)
            f.write(body)
            f.truncate()
        print(current_basepath, '->', basepath)
        print('M  ', default_file)

    def pull(self, dependencies=[], force=False, prefix=None, basepath=None):
        """Pull API Proxy revision and its dependencies from Apigee.

        Args:
            dependencies (list, optional): Initial list of dependencies to ``pull`` from Apigee. Defaults to ``[]``.
            force (bool, optional): If True, overwrite existing files. Defaults to False.
            prefix (str, optional): Prefix to add. Defaults to None.
            basepath (str, optional): New basepath to overwrite the existing one. Defaults to None.

        Returns:
            requests.Response(), list, list: exported API Proxy, KeyValueMaps, Targetservers
        """
        apis = Apis(self._auth, self._org_name, self._api_name)
        dependencies.append(self._api_name)

        makedirs(self._work_tree)

        if not force:
            paths_exist([self._zip_file, self._apiproxy_dir])

        print('Writing ZIP to', os.path.abspath(self._zip_file))
        export = apis.export_api_proxy(self._revision_number, write=True, output_file=self._zip_file)

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

        return export, keyvaluemaps, targetservers
