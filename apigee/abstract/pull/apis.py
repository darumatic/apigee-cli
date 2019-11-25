#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import os
from abc import ABC, abstractmethod
from pathlib import Path

from apigee.util.io import IO

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

    @abstractmethod
    def get_apiproxy_files(self, directory):
        pass

    @abstractmethod
    def get_keyvaluemap_dependencies(self, files):
        pass

    @abstractmethod
    def export_keyvaluemap_dependencies(self, args, kvms, kvms_dir, force=False):
        pass

    @abstractmethod
    def get_targetserver_dependencies(self, files):
        pass

    @abstractmethod
    def export_targetserver_dependencies(self, args, target_servers, target_servers_dir, force=False):
        pass

    @abstractmethod
    def prefix_dependencies_in_work_tree(self):
        pass

    @abstractmethod
    def get_apiproxy_basepath(self, directory):
        pass

    @abstractmethod
    def set_apiproxy_basepath(self, basepath, file):
        pass

    @abstractmethod
    def pull(self):
        pass
