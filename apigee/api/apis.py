#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.api.deployments import Deployments
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
    for i in Deployments(args).get_api_proxy_deployment_details().json()['environment']:
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

def export_api_proxy(args, write_zip=True):
    uri = '{}/v1/organizations/{}/apis/{}/revisions/{}?format=bundle'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name, args.revision_number)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if write_zip:
        zname = args.name + '.zip' if args.output_file is None else args.output_file
        with open(zname, 'wb') as zfile:
            zfile.write(resp.content)
    return resp

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
