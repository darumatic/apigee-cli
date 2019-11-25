#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import json
import os
import requests
import sys
import xml.etree.ElementTree as et
import zipfile
from pathlib import Path

from apigee.abstract.pull.apis import IPull
from apigee.api.apis import export_api_proxy
from apigee.api.keyvaluemaps import get_keyvaluemap_in_an_environment
from apigee.api.targetservers import get_targetserver

class Pull(IPull):

    def __init__(self, args):
        super().__init__(args)

    def get_apiproxy_files(self, directory):
        files = []
        for filename in Path(directory+'/apiproxy/').resolve().rglob('*'):
            files.append(str(filename))
        return files

    def get_keyvaluemap_dependencies(self, files):
        kvms = []
        for f in files:
            try:
                root = et.parse(f).getroot()
                if root.tag == 'KeyValueMapOperations':
                    kvms.append(root.attrib['mapIdentifier'])
            except:
                pass
        return kvms

    def export_keyvaluemap_dependencies(self, args, kvms, kvms_dir, force=False):
        if not os.path.exists(kvms_dir):
            os.makedirs(kvms_dir)
        for kvm in kvms:
            kvm_file = kvms_dir+'/'+kvm
            if not force:
                self.path_exists(kvm_file)
            print('Pulling', kvm, 'and writing to', os.path.abspath(kvm_file))
            args.name = kvm
            resp = get_keyvaluemap_in_an_environment(args).text
            print(resp)
            with open(kvm_file, 'w') as f:
                f.write(resp)

    def get_targetserver_dependencies(self, files):
        target_servers = []
        for f in files:
            try:
                root = et.parse(f).getroot()
                for child in root.iter('Server'):
                    target_servers.append(child.attrib['name'])
            except:
                pass
        return target_servers

    def export_targetserver_dependencies(self, args, target_servers, target_servers_dir, force=False):
        if not os.path.exists(target_servers_dir):
            os.makedirs(target_servers_dir)
        for ts in target_servers:
            ts_file = target_servers_dir+'/'+ts
            if not force:
                self.path_exists(ts_file)
            print('Pulling', ts, 'and writing to', os.path.abspath(ts_file))
            args.name = ts
            resp = get_targetserver(args).text
            print(resp)
            with open(ts_file, 'w') as f:
                f.write(resp)

    def prefix_dependencies_in_work_tree(self):
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
                        print('M  ', os.path.abspath(file))

    def get_apiproxy_basepath(self, directory):
        default_file = directory+'/apiproxy/proxies/default.xml'
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

    def pull(self):
        args = self._args
        dependencies = []

        if self._work_tree:
            self.makedirs(self._work_tree)

        directory = self._apiproxy_dir
        zip_file = directory + '.zip'

        if not args.force:
            self.paths_exist([zip_file, directory])

        print('Writing ZIP to', os.path.abspath(zip_file))
        self.writezip(zip_file, export_api_proxy(args, write_zip=False).content)

        self.makedirs(directory)

        print('Extracting', zip_file, 'in', os.path.abspath(directory))
        self.extractzip(zip_file, directory)

        os.remove(zip_file)

        files = self.get_apiproxy_files(directory)

        kvms = self.get_keyvaluemap_dependencies(files)

        print('KeyValueMap dependencies found:', kvms)
        dependencies.extend(kvms)

        self.export_keyvaluemap_dependencies(args, kvms, self._keyvaluemaps_dir, args.force)

        target_servers = self.get_targetserver_dependencies(files)

        print('TargetServer dependencies found:', target_servers)
        dependencies.extend(target_servers)

        self.export_targetserver_dependencies(args, target_servers, self._targetservers_dir, args.force)

        self._dependencies.extend(dependencies)
        self._dependencies = list(set(self._dependencies))

        if args.prefix:
            self.prefix_dependencies_in_work_tree()

        if args.basepath:
            basepath, file = self.get_apiproxy_basepath(directory)
            self.set_apiproxy_basepath(args.basepath, file)
