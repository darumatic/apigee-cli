#!/usr/bin/env python
"""https://apidocs.apigee.com/api/developers-0"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def list_developers(args):
    uri = '{}/v1/organizations/{}/developers?expand={}&count={}&startKey={}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.expand, args.count, args.startkey)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.prefix:
        return json.dumps([i for i in resp.json() if i.startswith(args.prefix)])
    return resp.text
