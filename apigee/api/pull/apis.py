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

def get_keyvaluemap_dependencies(args):
    pass

def get_targetserver_dependencies(args):
    pass

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
        if not os.path.exists(args.work_tree):
            os.makedirs(args.work_tree)
        os.chdir(args.work_tree)

    dname = args.name
    zname = dname + '.zip'

    if not args.force:
        if os.path.exists(zname):
            print('error:', zname, 'already exists')
            sys.exit(1)
        if os.path.exists(dname):
            print('error:', dname, 'already exists')
            sys.exit(1)

    with open(zname, 'wb') as zfile:
        print('Writing ZIP to', zname)
        zfile.write(resp.content)

    if not os.path.exists(dname):
        os.makedirs(dname)

    with zipfile.ZipFile(zname, 'r') as zip_ref:
        print('Extracting ZIP in', dname)
        zip_ref.extractall(dname)

    os.remove(zname)

    files = []
    for filename in Path(dname+'/apiproxy/').resolve().rglob('*'):
        files.append(str(filename))

    kvms = []
    for f in files:
        try:
            root = et.parse(f).getroot()
            if root.tag == 'KeyValueMapOperations':
                kvms.append(root.attrib['mapIdentifier'])
        except:
            pass

    print('KeyValueMap dependencies found:', kvms)
    dependencies.extend(kvms)

    kvms_dir = 'keyvaluemaps/'+args.environment
    if not os.path.exists(kvms_dir):
        os.makedirs(kvms_dir)

    for kvm in kvms:
        kvm_file = kvms_dir+'/'+kvm
        if not args.force:
            if os.path.exists(kvm_file):
                print('error:', kvm_file, 'already exists')
                sys.exit(1)
        print('Pulling', kvm, 'and writing to', kvm_file)
        args.name = kvm
        resp = get_keyvaluemap_in_an_environment(args).text
        print(resp)
        with open(kvm_file, 'w') as f:
            f.write(resp)

    target_servers = []
    for f in files:
        try:
            root = et.parse(f).getroot()
            for child in root.iter('Server'):
                target_servers.append(child.attrib['name'])
        except:
            pass

    print('TargetServer dependencies found:', target_servers)
    dependencies.extend(target_servers)

    target_servers_dir = 'targetservers/'+args.environment
    if not os.path.exists(target_servers_dir):
        os.makedirs(target_servers_dir)

    for ts in target_servers:
        ts_file = target_servers_dir+'/'+ts
        if not args.force:
            if os.path.exists(ts_file):
                print('error:', ts_file, 'already exists')
                sys.exit(1)
        print('Pulling', ts, 'and writing to', ts_file)
        args.name = ts
        resp = get_targetserver(args).text
        print(resp)
        with open(ts_file, 'w') as f:
            f.write(resp)

    if args.prefix:
        prefix_files(dependencies, args.prefix, os.getcwd())

    os.chdir(cwd)
