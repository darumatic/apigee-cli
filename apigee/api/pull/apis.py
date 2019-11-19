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
from apigee.api.keyvaluemaps import get_keyvaluemap_in_an_environment
from apigee.api.targetservers import get_targetserver
from apigee.util import authorization
from apigee.util import resolve_file

class Pull:

    def __init__(self, args):
        self._args = args
        if args.work_tree:
            if not os.path.exists(args.work_tree):
                os.makedirs(args.work_tree)
            self._work_tree = str(Path(args.work_tree).resolve())
        else:
            self._work_tree = os.getcwd()
        self._dependencies = []
        self._dependencies.append(args.name)
        self._prefix = args.prefix
        self._keyvaluemaps_dir = self._work_tree+'/keyvaluemaps/'+args.environment
        self._targetservers_dir = self._work_tree+'/targetservers/'+args.environment
        self._apiproxy_dir = self._work_tree+'/'+args.name

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @property
    def work_tree(self):
        return self._work_tree

    @work_tree.setter
    def work_tree(self, value):
        self._work_tree = value

    def __call__(self):
        self._pull()

    def _create_work_tree(self, work_tree):
        if not os.path.exists(work_tree):
            os.makedirs(work_tree)

    def _check_file_exists(self, file):
        if os.path.exists(file):
            sys.exit('error: ' + resolve_file(file) + ' already exists')

    def _check_files_exist(self, files):
        for file in files:
            self._check_file_exists(file)

    def _write_zip_file(self, file, content):
        print('Writing ZIP to', resolve_file(file))
        with open(file, 'wb') as zfile:
            zfile.write(content)

    def _create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _extract_zip_file(self, source, dest):
        print('Extracting ZIP in', resolve_file(dest))
        with zipfile.ZipFile(source, 'r') as zip_ref:
            zip_ref.extractall(dest)

    def _get_apiproxy_files(self, directory):
        files = []
        for filename in Path(directory+'/apiproxy/').resolve().rglob('*'):
            files.append(str(filename))
        return files

    def _get_keyvaluemap_dependencies(self, files):
        kvms = []
        for f in files:
            try:
                root = et.parse(f).getroot()
                if root.tag == 'KeyValueMapOperations':
                    kvms.append(root.attrib['mapIdentifier'])
            except:
                pass
        return kvms

    def _export_keyvaluemap_dependencies(self, args, kvms, kvms_dir, force=False):
        if not os.path.exists(kvms_dir):
            os.makedirs(kvms_dir)
        for kvm in kvms:
            kvm_file = kvms_dir+'/'+kvm
            if not force:
                self._check_file_exists(kvm_file)
            print('Pulling', kvm, 'and writing to', resolve_file(kvm_file))
            args.name = kvm
            resp = get_keyvaluemap_in_an_environment(args).text
            print(resp)
            with open(kvm_file, 'w') as f:
                f.write(resp)

    def _get_targetserver_dependencies(self, files):
        target_servers = []
        for f in files:
            try:
                root = et.parse(f).getroot()
                for child in root.iter('Server'):
                    target_servers.append(child.attrib['name'])
            except:
                pass
        return target_servers

    def _export_targetserver_dependencies(self, args, target_servers, target_servers_dir, force=False):
        if not os.path.exists(target_servers_dir):
            os.makedirs(target_servers_dir)
        for ts in target_servers:
            ts_file = target_servers_dir+'/'+ts
            if not force:
                self._check_file_exists(ts_file)
            print('Pulling', ts, 'and writing to', resolve_file(ts_file))
            args.name = ts
            resp = get_targetserver(args).text
            print(resp)
            with open(ts_file, 'w') as f:
                f.write(resp)

    def _prefix_dependencies_in_work_tree(self):
        prefix = self._prefix
        dependencies = [i for i in self._dependencies if not i.startswith(prefix)]
        directory = self._work_tree
        files = []
        for filename in Path(directory).resolve().rglob('*'):
            if not os.path.isdir(str(filename)) and '.git' not in str(filename):
                files.append(str(filename))
        print('Prefixing', dependencies, 'with', prefix)
        for dep in dependencies:
            for file in files:
                with open(file, 'r') as f:
                    body = None
                    try:
                        body = f.read()
                    except Exception as e:
                        print(type(e).__name__, e)
                        print('Ignoring', file)
                    if dep in body:
                        with open(file, 'w') as new_f:
                            new_f.write(body.replace(dep, prefix+dep))
                        print('M  ', resolve_file(file))

    def _get_apiproxy_basepath(self, directory):
        default_file = directory+'/apiproxy/proxies/default.xml'
        tree = et.parse(default_file)
        try:
            return tree.find('.//BasePath').text, default_file
        except AttributeError as ae:
            sys.exit('No BasePath found in ' + default_file)

    def _set_apiproxy_basepath(self, basepath, file):
        default_file = resolve_file(file)
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

    def _pull(self):

        args = self._args
        dependencies = []

        uri = '{}/v1/organizations/{}/apis/{}/revisions/{}?format=bundle'.format(
            APIGEE_ADMIN_API_URL, args.org, args.name, args.revision_number)
        hdrs = authorization.set_header({'Accept': 'application/json'}, args)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()

        if self._work_tree:
            self._create_work_tree(self._work_tree)

        directory = self._apiproxy_dir
        zip_file = directory + '.zip'

        if not args.force:
            self._check_files_exist([zip_file, directory])

        self._write_zip_file(zip_file, resp.content)

        self._create_directory(directory)

        self._extract_zip_file(zip_file, directory)

        os.remove(zip_file)

        files = self._get_apiproxy_files(directory)

        kvms = self._get_keyvaluemap_dependencies(files)

        print('KeyValueMap dependencies found:', kvms)
        dependencies.extend(kvms)

        self._export_keyvaluemap_dependencies(args, kvms, self._keyvaluemaps_dir, args.force)

        target_servers = self._get_targetserver_dependencies(files)

        print('TargetServer dependencies found:', target_servers)
        dependencies.extend(target_servers)

        self._export_targetserver_dependencies(args, target_servers, self._targetservers_dir, args.force)

        self._dependencies.extend(dependencies)
        self._dependencies = list(set(self._dependencies))

        if args.prefix:
            self._prefix_dependencies_in_work_tree()

        if args.basepath:
            basepath, file = self._get_apiproxy_basepath(directory)
            self._set_apiproxy_basepath(args.basepath, file)
