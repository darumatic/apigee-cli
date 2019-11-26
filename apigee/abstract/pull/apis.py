#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import os
from abc import ABC, abstractmethod
from pathlib import Path

class IPull:

    def __init__(self, args, api_name, revision_number, work_tree=None):
        self._args = args
        if work_tree:
            if not os.path.exists(work_tree):
                os.makedirs(work_tree)
            self._work_tree = str(Path(work_tree).resolve())
        else:
            self._work_tree = os.getcwd()
        self._api_name = api_name
        self._revision_number = revision_number
        self._keyvaluemaps_dir = self._work_tree+'/keyvaluemaps/'+args.environment
        self._targetservers_dir = self._work_tree+'/targetservers/'+args.environment
        self._apiproxy_dir = self._work_tree+'/'+args.name
        self._zip_file = self._apiproxy_dir+'.zip'

    def __call__(self, *args, **kwargs):
        self.pull(*args, **kwargs)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @property
    def api_name(self):
        return self._api_name

    @api_name.setter
    def api_name(self, value):
        self._api_name = value

    @property
    def revision_number(self):
        return self._revision_number

    @revision_number.setter
    def revision_number(self, value):
        self._revision_number = value

    @property
    def work_tree(self):
        return self._work_tree

    @work_tree.setter
    def work_tree(self, value):
        self._work_tree = value

    @abstractmethod
    def get_apiproxy_files(self, directory):
        pass

    @abstractmethod
    def get_keyvaluemap_dependencies(self, files):
        pass

    @abstractmethod
    def export_keyvaluemap_dependencies(self, args, keyvaluemaps, force=False):
        pass

    @abstractmethod
    def get_targetserver_dependencies(self, files):
        pass

    @abstractmethod
    def export_targetserver_dependencies(self, args, target_servers, force=False):
        pass

    @abstractmethod
    def prefix_dependencies_in_work_tree(self, dependencies, prefix):
        pass

    @abstractmethod
    def get_apiproxy_basepath(self, directory):
        pass

    @abstractmethod
    def set_apiproxy_basepath(self, basepath, file):
        pass

    @abstractmethod
    def pull(self, dependencies=[], force=False, prefix=None, basepath=None):
        pass
