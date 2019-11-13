#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import json
import os
import requests
import sys
import xml.etree.ElementTree as et
import zipfile
from pathlib import Path

from apigee import APIGEE_ADMIN_API_URL
from apigee.api.apis import delete_api_proxy_revision
from apigee.api.deployments import get_api_proxy_deployment_details
from apigee.api.keyvaluemaps import get_keyvaluemap_in_an_environment
from apigee.api.targetservers import get_targetserver
from apigee.util import authorization

def prefix_files(string_list, prefix, directory):
    string_list = [i for i in string_list if not i.startswith(prefix)]
    files = []
    for filename in Path(directory).resolve().rglob('*'):
        if not os.path.isdir(str(filename)) and '/.git/' not in str(filename):
            files.append(str(filename))
    print('Prefixing', string_list, 'with', prefix)
    for string in string_list:
        for file in files:
            with open(file, 'r') as f:
                body = None
                try:
                    body = f.read()
                except Exception as e:
                    print(type(e).__name__, e)
                    print('Ignoring', file)
                if body:
                    if string in body:
                        with open(file, 'w') as new_f:
                            new_f.write(body.replace(string, prefix+string))
                        print('M  ', file)

def create_work_tree(work_tree):
    if not os.path.exists(work_tree):
        os.makedirs(work_tree)

def check_files_exist(files):
    for file in files:
        if os.path.exists(file):
            print('error:', file, 'already exists')
            sys.exit(1)

def write_zip_file(file, content):
    with open(file, 'wb') as zfile:
        print('Writing ZIP to', file)
        zfile.write(content)

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def extract_zip_file(source, dest):
    with zipfile.ZipFile(source, 'r') as zip_ref:
        print('Extracting ZIP in', dest)
        zip_ref.extractall(dest)

def get_apiproxy_files(directory):
    files = []
    for filename in Path(directory+'/apiproxy/').resolve().rglob('*'):
        files.append(str(filename))
    return files

def get_keyvaluemap_dependencies(files):
    kvms = []
    for f in files:
        try:
            root = et.parse(f).getroot()
            if root.tag == 'KeyValueMapOperations':
                kvms.append(root.attrib['mapIdentifier'])
        except:
            pass
    return kvms

def export_keyvaluemap_dependencies(args, kvms, kvms_dir, force=False):
    if not os.path.exists(kvms_dir):
        os.makedirs(kvms_dir)
    for kvm in kvms:
        kvm_file = kvms_dir+'/'+kvm
        if not force:
            if os.path.exists(kvm_file):
                print('error:', kvm_file, 'already exists')
                sys.exit(1)
        print('Pulling', kvm, 'and writing to', kvm_file)
        args.name = kvm
        resp = get_keyvaluemap_in_an_environment(args).text
        print(resp)
        with open(kvm_file, 'w') as f:
            f.write(resp)

def get_targetserver_dependencies(files):
    target_servers = []
    for f in files:
        try:
            root = et.parse(f).getroot()
            for child in root.iter('Server'):
                target_servers.append(child.attrib['name'])
        except:
            pass
    return target_servers

def export_targetserver_dependencies(args, target_servers, target_servers_dir, force=False):
    if not os.path.exists(target_servers_dir):
        os.makedirs(target_servers_dir)
    for ts in target_servers:
        ts_file = target_servers_dir+'/'+ts
        if not force:
            if os.path.exists(ts_file):
                print('error:', ts_file, 'already exists')
                sys.exit(1)
        print('Pulling', ts, 'and writing to', ts_file)
        args.name = ts
        resp = get_targetserver(args).text
        print(resp)
        with open(ts_file, 'w') as f:
            f.write(resp)

def pull(args):

    dependencies = []
    dependencies.append(args.name)

    uri = '{}/v1/organizations/{}/apis/{}/revisions/{}?format=bundle'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name, args.revision_number)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()

    cwd = os.getcwd()

    if args.work_tree:
        create_work_tree(args.work_tree)
        os.chdir(args.work_tree)

    dname = args.name
    zname = dname + '.zip'

    if not args.force:
        check_files_exist([zname, dname])

    write_zip_file(zname, resp.content)

    create_directory(dname)

    extract_zip_file(zname, dname)

    os.remove(zname)

    files = get_apiproxy_files(dname)

    kvms = get_keyvaluemap_dependencies(files)

    print('KeyValueMap dependencies found:', kvms)
    dependencies.extend(kvms)

    export_keyvaluemap_dependencies(args, kvms, 'keyvaluemaps/'+args.environment, args.force)

    target_servers = get_targetserver_dependencies(files)

    print('TargetServer dependencies found:', target_servers)
    dependencies.extend(target_servers)

    export_targetserver_dependencies(args, target_servers, 'targetservers/'+args.environment, args.force)

    if args.prefix:
        prefix_files(list(set(dependencies)), args.prefix, os.getcwd())

    os.chdir(cwd)
