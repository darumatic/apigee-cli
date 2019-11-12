#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import os
import requests
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as et
import zipfile

from apigee import APIGEE_ADMIN_API_URL
from apigee.api.deployments import get_api_proxy_deployment_details
from apigee.api.keyvaluemaps import get_keyvaluemap_in_an_environment
from apigee.api.targetservers import get_targetserver
from apigee.util import authorization

def delete_api_proxy_revision(args):
    uri = '{}/v1/organizations/{}/apis/{}/revisions/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name, args.revision_number)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.delete(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def delete_undeployed_revisions(args):
    revisions = list_api_proxy_revisions(args).json()
    deployment_details = []
    for i in get_api_proxy_deployment_details(args).json()['environment']:
        deployment_details.append({
            'name':i['name'],'revision':[
                j['name'] for j in i['revision']
            ]
        })
    deployed = []
    for dep in deployment_details:
        deployed.extend(dep['revision'])
    deployed = list(set(deployed))
    undeployed = [rev for rev in revisions if rev not in deployed]
    undeployed = [int(x) for x in undeployed]
    undeployed.sort()
    undeployed = undeployed[:len(undeployed)-args.save_last]
    print('Undeployed revisions:', undeployed)
    if not args.dry_run:
        for rev in undeployed:
            args.revision_number = rev
            print('Deleting revison', rev)
            delete_api_proxy_revision(args)

def export_api_proxy(args):
    uri = '{}/v1/organizations/{}/apis/{}/revisions/{}?format=bundle'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name, args.revision_number)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    zname = args.name + '.zip' if args.output_file is None else args.output_file
    with open(zname, 'wb') as zfile:
        zfile.write(resp.content)

def pull(args):
    uri = '{}/v1/organizations/{}/apis/{}/revisions/{}?format=bundle'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name, args.revision_number)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)

    cwd = os.getcwd()

    if args.work_tree:
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

    os.chdir(cwd)

def get_api_proxy(args):
    uri = '{}/v1/organizations/{}/apis/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def list_api_proxies(args):
    uri = '{}/v1/organizations/{}/apis'.format(
        APIGEE_ADMIN_API_URL, args.org)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.prefix:
        return json.dumps([i for i in resp.json() if i.startswith(args.prefix)])
    return resp.text

def list_api_proxy_revisions(args):
    uri = '{}/v1/organizations/{}/apis/{}/revisions'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp
