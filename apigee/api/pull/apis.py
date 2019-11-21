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

class Pull(IPull):

    def __init__(self, args):
        super().__init__(args)

    def pull(self):
        args = self._args
        dependencies = []

        if self._work_tree:
            self._create_work_tree(self._work_tree)

        directory = self._apiproxy_dir
        zip_file = directory + '.zip'

        if not args.force:
            self._check_files_exist([zip_file, directory])

        self._write_zip_file(zip_file, export_api_proxy(args, write_zip=False).content)

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
