#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

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
