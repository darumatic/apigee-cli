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
# from apigee.api.apis import export_api_proxy
from apigee.api.apis import Apis
from apigee.api.keyvaluemaps import get_keyvaluemap_in_an_environment
from apigee.api.targetservers import get_targetserver
from apigee.util.os import (
    makedirs,
    path_exists,
    paths_exist,
    extractzip,
    writezip
)

class Pull(IPull):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_apiproxy_files(self, directory):
        files = []
        for filename in Path(directory+'/apiproxy/').resolve().rglob('*'):
            files.append(str(filename))
        return files

    def get_keyvaluemap_dependencies(self, files):
        keyvaluemaps = []
        for f in files:
            try:
                root = et.parse(f).getroot()
                if root.tag == 'KeyValueMapOperations':
                    keyvaluemaps.append(root.attrib['mapIdentifier'])
            except:
                pass
        return keyvaluemaps

    def export_keyvaluemap_dependencies(self, args, keyvaluemaps, force=False):
        makedirs(self._keyvaluemaps_dir)
        for keyvaluemap in keyvaluemaps:
            keyvaluemap_file = self._keyvaluemaps_dir+'/'+keyvaluemap
            if not force:
                path_exists(keyvaluemap_file)
            print('Pulling', keyvaluemap, 'and writing to', os.path.abspath(keyvaluemap_file))
            args.name = keyvaluemap
            resp = get_keyvaluemap_in_an_environment(args).text
            print(resp)
            with open(keyvaluemap_file, 'w') as f:
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

    def export_targetserver_dependencies(self, args, target_servers, force=False):
        makedirs(self._targetservers_dir)
        for ts in target_servers:
            ts_file = self._targetservers_dir+'/'+ts
            if not force:
                path_exists(ts_file)
            print('Pulling', ts, 'and writing to', os.path.abspath(ts_file))
            args.name = ts
            resp = get_targetserver(args).text
            print(resp)
            with open(ts_file, 'w') as f:
                f.write(resp)

    def prefix_dependencies_in_work_tree(self, dependencies, prefix):
        dependencies = [i for i in dependencies if not i.startswith(prefix)]
        directory = self._work_tree
        files = []
        for filename in Path(directory).resolve().rglob('*'):
            if not os.path.isdir(str(filename)) and '.git' not in str(filename):
                files.append(str(filename))
        print('Prefixing', dependencies, 'with', prefix)
        for dep in dependencies:
            for file in files:
                with open(file, 'r') as f:
                    body = str()
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

    def pull(self, dependencies=[], force=False, prefix=None, basepath=None):
        dependencies.append(self._api_name)

        if self._work_tree:
            makedirs(self._work_tree)

        if not force:
            paths_exist([self._zip_file, self._apiproxy_dir])

        print('Writing ZIP to', os.path.abspath(self._zip_file))
        writezip(self._zip_file, Apis(self._args, self._args.org, self._api_name).export_api_proxy(self._revision_number, writezip=False).content)

        makedirs(self._apiproxy_dir)

        print('Extracting', self._zip_file, 'in', os.path.abspath(self._apiproxy_dir))
        extractzip(self._zip_file, self._apiproxy_dir)

        os.remove(self._zip_file)

        files = self.get_apiproxy_files(self._apiproxy_dir)

        keyvaluemaps = self.get_keyvaluemap_dependencies(files)

        print('KeyValueMap dependencies found:', keyvaluemaps)
        dependencies.extend(keyvaluemaps)

        self.export_keyvaluemap_dependencies(self._args, keyvaluemaps, force=force)

        target_servers = self.get_targetserver_dependencies(files)

        print('TargetServer dependencies found:', target_servers)
        dependencies.extend(target_servers)

        self.export_targetserver_dependencies(self._args, target_servers, force=force)

        if prefix:
            self.prefix_dependencies_in_work_tree(list(set(dependencies)), prefix)

        if basepath:
            basepath, file = self.get_apiproxy_basepath(self._apiproxy_dir)
            self.set_apiproxy_basepath(basepath, file)
