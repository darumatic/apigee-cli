import json
import os
from pathlib import Path


class InformalPullInterface:
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
        self._keyvaluemaps_dir = str(Path(self._work_tree) / 'keyvaluemaps' / environment)
        self._targetservers_dir = str(Path(self._work_tree) / 'targetservers' / environment)
        self._caches_dir = str(Path(self._work_tree) / 'caches' / environment)
        self._apiproxy_dir = str(Path(self._work_tree))
        self._zip_file = str(Path(self._apiproxy_dir).with_suffix('.zip'))

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
    def caches_dir(self):
        return self._caches_dir

    @caches_dir.setter
    def caches_dir(self, value):
        self._caches_dir = str(Path(self._work_tree) / value / environment)

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
