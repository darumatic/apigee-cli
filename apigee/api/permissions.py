#!/usr/bin/env python
"""https://docs.apigee.com/api-platform/system-administration/permissions"""

import requests
import json

import pandas as pd
from pandas.io.json import json_normalize

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def create_permissions(args):
    uri = '{}/v1/organizations/{}/userroles/{}/resourcepermissions'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = json.loads(args.body)
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def get_permissions(args):
    uri = '{}/v1/o/{}/userroles/{}/permissions'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.no_table:
        return resp.text
    return pd.DataFrame.from_dict(json_normalize(resp.json()['resourcePermission']), orient='columns')
