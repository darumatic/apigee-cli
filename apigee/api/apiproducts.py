#!/usr/bin/env python
"""https://apidocs.apigee.com/api/api-products-1"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def get_api_product(args):
    uri = '{}/v1/organizations/{}/apiproducts/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def list_api_products(args):
    uri = '{}/v1/organizations/{}/apiproducts?expand={}&count={}&startKey={}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.expand, args.count, args.startkey)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.prefix:
        return json.dumps([i for i in resp.json() if i.startswith(args.prefix)])
    return resp.text
