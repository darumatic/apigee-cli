#!/usr/bin/env python
"""https://apidocs.apigee.com/api/deployments"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def get_api_proxy_deployment_details(args):
    uri = '{}/v1/organizations/{}/apis/{}/deployments'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.revision_name:
        return json.dumps([{i['name']:[j['name'] for j in i['revision']]} for i in resp.json()['environment']])
    return resp.text
