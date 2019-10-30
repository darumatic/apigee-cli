#!/usr/bin/env python
"""https://docs.apigee.com/api-platform/system-administration/permissions"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def get_permissions(args):
    uri = '{}/v1/o/{}/userroles/{}/permissions'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp
