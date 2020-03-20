#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

# from apigee.util.os import serializepath, splitpath


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

    @abstractmethod
    def delete_api_proxy_revision(self, api_name, revision_number):
        pass

    @abstractmethod
    def deploy_api_proxy_revision(
        self, api_name, environment, revision_number, delay=0, override=False
    ):
        pass

    @abstractmethod
    def delete_undeployed_revisions(self, api_name, save_last=0, dry_run=False):
        pass

    @abstractmethod
    def export_api_proxy(
        self, api_name, revision_number, fs_write=True, write=True, output_file=None
    ):
        pass

    @abstractmethod
    def get_api_proxy(self, api_name):
        pass

    @abstractmethod
    def list_api_proxies(self, prefix=None):
        pass

    @abstractmethod
    def list_api_proxy_revisions(self, api_name):
        pass

    @abstractmethod
    def undeploy_api_proxy_revision(self, api_name, environment, revision_number):
        pass

    @abstractmethod
    def force_undeploy_api_proxy_revision(self, api_name, environment, revision_number):
        pass


class ApisSerializer:
    def serialize_details(self, apis, format, prefix=None):
        resp = apis
        if format == "text":
            return apis.text
        apis = apis.json()
        if prefix:
            apis = [api for api in apis if api.startswith(prefix)]
        if format == "json":
            return json.dumps(apis)
        elif format == "table":
            pass
        # else:
        #     raise ValueError(format)
        return resp


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
        self._keyvaluemaps_dir = str(
            Path(self._work_tree) / "keyvaluemaps" / environment
        )
        self._targetservers_dir = str(
            Path(self._work_tree) / "targetservers" / environment
        )
        # self._apiproxy_dir = str(Path(self._work_tree) / api_name)
        self._apiproxy_dir = str(Path(self._work_tree))
        self._zip_file = str(Path(self._apiproxy_dir).with_suffix(".zip"))

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

    @abstractmethod
    def get_apiproxy_files(self, directory):
        pass

    @abstractmethod
    def get_keyvaluemap_dependencies(self, files):
        pass

    @abstractmethod
    def export_keyvaluemap_dependencies(self, environment, keyvaluemaps, force=False):
        pass

    @abstractmethod
    def get_targetserver_dependencies(self, files):
        pass

    @abstractmethod
    def export_targetserver_dependencies(
        self, environment, target_servers, force=False
    ):
        pass

    @abstractmethod
    def replace_substring(self, file, old, new):
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
    def pull(self, api_name, dependencies=[], force=False, prefix=None, basepath=None):
        pass
