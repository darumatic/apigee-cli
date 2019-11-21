#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import json
import os
import requests
import sys
import xml.etree.ElementTree as et
import zipfile
from abc import ABC, abstractmethod
from pathlib import Path

from apigee.util.io import IO
from apigee.api.keyvaluemaps import get_keyvaluemap_in_an_environment
from apigee.api.targetservers import get_targetserver

class IPull(IO):

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

    def __call__(self):
        self.pull()

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

    @property
    def dependencies(self):
        return self._dependencies

    @dependencies.setter
    def dependencies(self, value):
        self._dependencies = value

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value

    @property
    def keyvaluemaps_dir(self):
        return self._keyvaluemaps_dir

    @keyvaluemaps_dir.setter
    def keyvaluemaps_dir(self, value):
        self._keyvaluemaps_dir = value

    @property
    def targetservers_dir(self):
        return self._targetservers_dir

    @targetservers_dir.setter
    def targetservers_dir(self, value):
        self._targetservers_dir = value

    @property
    def apiproxy_dir(self):
        return self._apiproxy_dir

    @apiproxy_dir.setter
    def apiproxy_dir(self, value):
        self._apiproxy_dir = value

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
                self.check_file_exists(kvm_file)
            print('Pulling', kvm, 'and writing to', self.resolve_file(kvm_file))
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
                self.check_file_exists(ts_file)
            print('Pulling', ts, 'and writing to', self.resolve_file(ts_file))
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
                        print('M  ', self.resolve_file(file))

    def _get_apiproxy_basepath(self, directory):
        default_file = directory+'/apiproxy/proxies/default.xml'
        tree = et.parse(default_file)
        try:
            return tree.find('.//BasePath').text, default_file
        except AttributeError as ae:
            sys.exit('No BasePath found in ' + default_file)

    def _set_apiproxy_basepath(self, basepath, file):
        default_file = self.resolve_file(file)
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

    @abstractmethod
    def pull(self):
        pass
