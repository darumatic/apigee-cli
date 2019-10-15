#!/usr/bin/env python
"""https://apidocs.apigee.com/api/apps-developer"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def get_developer_app_details(args):
    uri = '{}/v1/organizations/{}/developers/{}/apps/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.developer, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def list_developer_apps(args):
    if args.expand:
        uri = '{}/v1/organizations/{}/developers/{}/apps?expand={}'.format(
            APIGEE_ADMIN_API_URL, args.org, args.developer, args.expand)
    else:
        uri = '{}/v1/organizations/{}/developers/{}/apps?count={}&startKey={}'.format(
            APIGEE_ADMIN_API_URL, args.org, args.developer, args.count, args.startkey)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.prefix:
        return json.dumps([i for i in resp.json() if i.startswith(args.prefix)])
    return resp.text
