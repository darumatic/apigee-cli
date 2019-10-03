#!/usr/bin/env python
"""https://apidocs.apigee.com/api/api_resources/51-targetservers"""

import requests

from apigeecli import APIGEE_ADMIN_API_URL
from apigeecli.util import authorization

def list_targetservers_in_an_environment(args):
    uri = '{}/v1/organizations/{}/environments/{}/targetservers'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def get_targetserver(args):
    uri = '{}/v1/organizations/{}/environments/{}/targetservers/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp
