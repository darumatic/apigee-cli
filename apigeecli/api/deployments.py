#!/usr/bin/env python
"""https://apidocs.apigee.com/api/deployments"""

import requests

from apigeecli import APIGEE_ADMIN_API_URL
from apigeecli.util import authorization

def get_api_proxy_deployment_details(args):
    uri = '{}/v1/organizations/{}/apis/{}/deployments'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name
    )
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    return resp
