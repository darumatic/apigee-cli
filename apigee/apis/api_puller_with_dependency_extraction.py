import logging
import os
import xml.etree.ElementTree as et
from pathlib import Path

from apigee import console
from apigee.apis.apis import Apis
from apigee.caches.caches import Caches
from apigee.keyvaluemaps.keyvaluemaps import Keyvaluemaps
from apigee.targetservers.targetservers import Targetservers
from apigee.utils import (extract_zip_file, create_directory, check_file_exists, check_files_exist,
                          execute_function_on_directory_files, apply_function_on_iterable)


import os
from pathlib import Path

class ApiPullerWithDependencyExtraction:
    def __init__(self, auth, org_name, revision_number, environment, working_directory=None):
        self.auth = auth
        self.org_name = org_name
        self.working_directory = working_directory
        self.revision_number = revision_number
        self.environment = environment
        self.keyvaluemaps_dir = "keyvaluemaps"
        self.targetservers_dir = "targetservers"
        self.caches_dir = "caches"
        self.apiproxy_dir = self.working_directory
        self.zip_file = str(Path(self.apiproxy_dir).with_suffix(".zip"))

    @property
    def working_directory(self):
        return self._working_directory

    @working_directory.setter
    def working_directory(self, value):
        if value:
            if not os.path.exists(value):
                os.makedirs(value)
            self._working_directory = str(Path(value).resolve())
        else:
            self._working_directory = os.getcwd()

    @property
    def keyvaluemaps_dir(self):
        return self._keyvaluemaps_dir

    @keyvaluemaps_dir.setter
    def keyvaluemaps_dir(self, value):
        self._keyvaluemaps_dir = str(Path(self._working_directory) / value / self.environment)

    @property
    def targetservers_dir(self):
        return self._targetservers_dir

    @targetservers_dir.setter
    def targetservers_dir(self, value):
        self._targetservers_dir = str(Path(self._working_directory) / value / self.environment)

    @property
    def caches_dir(self):
        return self._caches_dir

    @caches_dir.setter
    def caches_dir(self, value):
        self._caches_dir = str(Path(self._working_directory) / value / self.environment)

    @property
    def apiproxy_dir(self):
        return self._apiproxy_dir

    @apiproxy_dir.setter
    def apiproxy_dir(self, value):
        self._apiproxy_dir = str(Path(self._working_directory) / value)

    def export_and_extract_api_proxy(self, api_name, force=False):
        create_directory(self.working_directory)
        self.apiproxy_dir = api_name
        if not force:
            check_files_exist(
                (os.path.relpath(self.zip_file), os.path.relpath(self.apiproxy_dir))
            )
        exported_api = Apis(self.auth, self.org_name).export_api_proxy(
            api_name, self.revision_number, write_to_filesystem=True, output_file=self.zip_file
        )
        create_directory(self.apiproxy_dir)
        extract_zip_file(self.zip_file, self.apiproxy_dir)
        os.remove(self.zip_file)
        files = self.get_apiproxy_files(self.apiproxy_dir)
        for resource_type in ("keyvaluemap", "targetserver", "cache"):
            self.export_resource_dependencies_using_getattr(
                resource_type,
                files,
                self.environment,
                force=force,
            )
        return exported_api

    def export_cache_dependencies(
        self, environment, caches, force=False, expected_verbosity=1
    ):
        create_directory(self.caches_dir)

        def _func(cache):
            cache_file = str(Path(self.caches_dir) / f"{cache}.json")
            if not force:
                check_file_exists(os.path.relpath(cache_file))
            resp = (
                Caches(self.auth, self.org_name, cache)
                .get_information_about_a_cache(environment)
                .text
            )
            console.echo(resp, expected_verbosity=1)
            with open(cache_file, "w") as f:
                f.write(resp)

        return apply_function_on_iterable(caches, _func)

    def export_keyvaluemap_dependencies(
        self, environment, keyvaluemaps, force=False, expected_verbosity=1
    ):
        create_directory(self.keyvaluemaps_dir)

        def _func(kvm):
            kvm_file = str(Path(self.keyvaluemaps_dir) / f"{kvm}.json")
            if not force:
                check_file_exists(os.path.relpath(kvm_file))
            resp = (
                Keyvaluemaps(self.auth, self.org_name, kvm)
                .get_keyvaluemap_in_an_environment(environment)
                .text
            )
            console.echo(resp, expected_verbosity=1)
            with open(kvm_file, "w") as f:
                f.write(resp)

        return apply_function_on_iterable(keyvaluemaps, _func)

    def export_resource_dependencies_using_getattr(self, resource_type, files, environment, force=True):
        resource_files = getattr(self, f"get_{resource_type}_dependencies")(files)
        getattr(self, f"export_{resource_type}_dependencies")(
            environment, resource_files, force=force
        )
        return resource_files

    def export_targetserver_dependencies(
        self, environment, targetservers, force=False, expected_verbosity=1
    ):
        create_directory(self.targetservers_dir)

        def _func(ts):
            ts_file = str(Path(self.targetservers_dir) / f"{ts}.json")
            if not force:
                check_file_exists(os.path.relpath(ts_file))
            resp = (
                Targetservers(self.auth, self.org_name, ts)
                .get_targetserver(environment)
                .text
            )
            console.echo(resp, expected_verbosity=1)
            with open(ts_file, "w") as f:
                f.write(resp)

        return apply_function_on_iterable(targetservers, _func)

    def get_apiproxy_files(self, directory):
        return execute_function_on_directory_files(str(Path(directory) / "apiproxy"), lambda f: f)

    def get_cache_dependencies(self, files):
        def _func(f, _state):
            try:
                name = et.parse(f).find(".//CacheResource").text
                if name and name not in _state:
                    _state.add(name)
                    return name
            except Exception as e:
                logging.warning(f"{e}; file={f}", exc_info=True)

        return apply_function_on_iterable(files, _func, args=(set(),))

    def get_keyvaluemap_dependencies(self, files):
        def _func(f, _state):
            try:
                root = et.parse(f).getroot()
# sourcery skip: merge-nested-ifs
                if root.tag == "KeyValueMapOperations":
                    if root.attrib["mapIdentifier"] not in _state:
                        _state.add(root.attrib["mapIdentifier"])
                        return root.attrib["mapIdentifier"]
            except Exception as e:
                logging.warning(f"{e}; file={f}", exc_info=True)

        return apply_function_on_iterable(files, _func, args=(set(),))

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

        return apply_function_on_iterable(files, _func, args=(set(),))
