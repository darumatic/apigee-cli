import logging
import os
import xml.etree.ElementTree as et
from pathlib import Path

from apigee import console
from apigee.apis.apis import Apis
from apigee.caches.caches import Caches
from apigee.keyvaluemaps.keyvaluemaps import Keyvaluemaps
from apigee.targetservers.targetservers import Targetservers
from apigee.utils import (
    make_dirs,
    path_exists,
    paths_exist,
    run_func_on_dir_files,
    run_func_on_iterable,
    extract_zip,
)


class PullApis:
    def __init__(self, auth, org_name, revision_number, environment, work_tree=None):
        self.auth = auth
        self.org_name = org_name
        self.work_tree = work_tree
        self.revision_number = revision_number
        self.environment = environment
        self.keyvaluemaps_dir = "keyvaluemaps"
        self.targetservers_dir = "targetservers"
        self.caches_dir = "caches"
        self._apiproxy_dir = self.work_tree
        self.zip_file = str(Path(self.apiproxy_dir).with_suffix(".zip"))

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

    @property
    def work_tree(self):
        return self._work_tree

    @work_tree.setter
    def work_tree(self, value):
        if value:
            if not os.path.exists(value):
                os.makedirs(value)
            self._work_tree = str(Path(value).resolve())
        else:
            self._work_tree = os.getcwd()

    @property
    def keyvaluemaps_dir(self):
        return self._keyvaluemaps_dir

    @keyvaluemaps_dir.setter
    def keyvaluemaps_dir(self, value):
        self._keyvaluemaps_dir = str(Path(self.work_tree) / value / self.environment)

    @property
    def targetservers_dir(self):
        return self._targetservers_dir

    @targetservers_dir.setter
    def targetservers_dir(self, value):
        self._targetservers_dir = str(Path(self.work_tree) / value / self.environment)

    @property
    def caches_dir(self):
        return self._caches_dir

    @caches_dir.setter
    def caches_dir(self, value):
        self._caches_dir = str(Path(self.work_tree) / value / self.environment)

    @property
    def apiproxy_dir(self):
        return self._apiproxy_dir

    @apiproxy_dir.setter
    def apiproxy_dir(self, value):
        self._apiproxy_dir = str(Path(self.work_tree) / value)

    @property
    def zip_file(self):
        return self._zip_file

    @zip_file.setter
    def zip_file(self, value):
        self._zip_file = value

    # def call_export_method(self, resource_type, files, environment, dependencies=[], force=True):
    def call_export_method(self, resource_type, files, environment, force=True):
        resource_files = getattr(self, f"get_{resource_type}_dependencies")(files)
        # dependencies.extend(resource_files)
        getattr(self, f"export_{resource_type}_dependencies")(
            environment, resource_files, force=force
        )
        # return dependencies
        return resource_files

    def get_apiproxy_files(self, directory):
        return run_func_on_dir_files(str(Path(directory) / "apiproxy"), lambda f: f)

    def get_keyvaluemap_dependencies(self, files):
        def _func(f, _state):
            try:
                root = et.parse(f).getroot()
                if root.tag == "KeyValueMapOperations":
                    if root.attrib["mapIdentifier"] not in _state:
                        _state.add(root.attrib["mapIdentifier"])
                        return root.attrib["mapIdentifier"]
            except Exception as e:
                logging.warning(f"{e}; file={f}", exc_info=True)

        return run_func_on_iterable(files, _func, args=(set(),))

    def export_keyvaluemap_dependencies(
        self, environment, keyvaluemaps, force=False, expc_verbosity=1
    ):
        make_dirs(self._keyvaluemaps_dir)

        def _func(kvm):
            kvm_file = str(Path(self._keyvaluemaps_dir) / f"{kvm}.json")
            if not force:
                path_exists(os.path.relpath(kvm_file))
            resp = (
                Keyvaluemaps(self._auth, self._org_name, kvm)
                .get_keyvaluemap_in_an_environment(environment)
                .text
            )
            console.echo(resp, expc_verbosity=1)
            with open(kvm_file, "w") as f:
                f.write(resp)

        return run_func_on_iterable(keyvaluemaps, _func)

    def get_targetserver_dependencies(self, files):
        def _func(f, _state):
            try:
                root = et.parse(f).getroot()
                for child in root.iter("Server"):
                    if child.attrib["name"] not in _state:
                        _state.add(child.attrib["name"])
                        return child.attrib["name"]
            except Exception as e:
                logging.warning(f"{e}; file={f}", exc_info=True)

        return run_func_on_iterable(files, _func, args=(set(),))

    def export_targetserver_dependencies(
        self, environment, targetservers, force=False, expc_verbosity=1
    ):
        make_dirs(self._targetservers_dir)

        def _func(ts):
            ts_file = str(Path(self._targetservers_dir) / f"{ts}.json")
            if not force:
                path_exists(os.path.relpath(ts_file))
            resp = (
                Targetservers(self._auth, self._org_name, ts)
                .get_targetserver(environment)
                .text
            )
            console.echo(resp, expc_verbosity=1)
            with open(ts_file, "w") as f:
                f.write(resp)

        return run_func_on_iterable(targetservers, _func)

    def get_cache_dependencies(self, files):
        def _func(f, _state):
            try:
                name = et.parse(f).find(".//CacheResource").text
                if name and name not in _state:
                    _state.add(name)
                    return name
            except Exception as e:
                logging.warning(f"{e}; file={f}", exc_info=True)

        return run_func_on_iterable(files, _func, args=(set(),))

    def export_cache_dependencies(
        self, environment, caches, force=False, expc_verbosity=1
    ):
        make_dirs(self._caches_dir)

        def _func(cache):
            cache_file = str(Path(self._caches_dir) / f"{cache}.json")
            if not force:
                path_exists(os.path.relpath(cache_file))
            resp = (
                Caches(self._auth, self._org_name, cache)
                .get_information_about_a_cache(environment)
                .text
            )
            console.echo(resp, expc_verbosity=1)
            with open(cache_file, "w") as f:
                f.write(resp)

        return run_func_on_iterable(caches, _func)

    # def pull(self, api_name, dependencies=[], force=False, prefix=None, basepath=None):
    def pull(self, api_name, force=False):
        # dependencies.append(api_name)
        make_dirs(self.work_tree)
        self.apiproxy_dir = api_name
        if not force:
            paths_exist(
                (os.path.relpath(self.zip_file), os.path.relpath(self.apiproxy_dir))
            )
        exported_api = Apis(self.auth, self.org_name).export_api_proxy(
            api_name, self.revision_number, fs_write=True, output_file=self.zip_file
        )
        make_dirs(self.apiproxy_dir)
        extract_zip(self.zip_file, self.apiproxy_dir)
        os.remove(self.zip_file)
        files = self.get_apiproxy_files(self.apiproxy_dir)
        for resource_type in ("keyvaluemap", "targetserver", "cache"):
            self.call_export_method(
                # resource_type, files, self.environment, dependencies=dependencies, force=force
                resource_type,
                files,
                self.environment,
                force=force,
            )
        # print(dependencies)
        # return exported_api, dependencies
        return exported_api
