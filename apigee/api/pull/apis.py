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
from apigee.api.keyvaluemaps import get_keyvaluemap_in_an_environment
from apigee.api.targetservers import get_targetserver
from apigee.util import authorization
from apigee.util import resolve_file

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
                        print('M  ', resolve_file(file))

def create_work_tree(work_tree):
    if not os.path.exists(work_tree):
        os.makedirs(work_tree)

def check_files_exist(files):
    for file in files:
        if os.path.exists(file):
            print('error:', resolve_file(file), 'already exists')
            sys.exit(1)

def write_zip_file(file, content):
    print('Writing ZIP to', resolve_file(file))
    with open(file, 'wb') as zfile:
        zfile.write(content)

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def extract_zip_file(source, dest):
    print('Extracting ZIP in', resolve_file(dest))
    with zipfile.ZipFile(source, 'r') as zip_ref:
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
                print('error:', resolve_file(kvm_file), 'already exists')
                sys.exit(1)
        print('Pulling', kvm, 'and writing to', resolve_file(kvm_file))
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
                print('error:', resolve_file(ts_file), 'already exists')
                sys.exit(1)
        print('Pulling', ts, 'and writing to', resolve_file(ts_file))
        args.name = ts
        resp = get_targetserver(args).text
        print(resp)
        with open(ts_file, 'w') as f:
            f.write(resp)

def get_apiproxy_basepath(directory):
    default_file = directory+'/apiproxy/proxies/default.xml'
    tree = et.parse(default_file)
    try:
        return tree.find('.//BasePath').text, default_file
    except AttributeError as ae:
        print('No BasePath found in', default_file)
        sys.exit(1)

def set_apiproxy_basepath(basepath, file):
    default_file = resolve_file(file)
    tree = et.parse(default_file)
    current_basepath = None
    try:
        current_basepath = tree.find('.//BasePath').text
    except AttributeError as ae:
        print('No BasePath found in', default_file)
        sys.exit(1)
    with open(default_file, 'r+') as f:
        body = f.read().replace(current_basepath, basepath)
        f.seek(0)
        f.write(body)
        f.truncate()
    print(current_basepath, '->', basepath)
    print('M  ', default_file)

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

    directory = args.name
    zip_file = directory + '.zip'

    if not args.force:
        check_files_exist([zip_file, directory])

    write_zip_file(zip_file, resp.content)

    create_directory(directory)

    extract_zip_file(zip_file, directory)

    os.remove(zip_file)

    files = get_apiproxy_files(directory)

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

    if args.basepath:
        basepath, file = get_apiproxy_basepath(directory)
        set_apiproxy_basepath(args.basepath, file)

    os.chdir(cwd)
