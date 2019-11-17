#!/usr/bin/env python
"""https://apidocs.apigee.com/api/deployments"""

import requests
import json

import pandas as pd
from pandas.io.json import json_normalize

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization
from apigee.wrappers.deployments import get_api_proxy_deployment_details

@get_api_proxy_deployment_details
def get_api_proxy_deployment_details(args):
    uri = '{}/v1/organizations/{}/apis/{}/deployments'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def get_api_proxy_deployment_details_formatted(args):
    resp = get_api_proxy_deployment_details(args)
    if args.revision_name:
        revisions = []
        for i in resp.json()['environment']:
            revisions.append({
                'name':i['name'],'revision':[
                    j['name'] for j in i['revision']
                ]
            })
        if args.json:
            return json.dumps(revisions)
        pd.set_option('display.max_colwidth', args.max_colwidth)
        return pd.DataFrame.from_dict(json_normalize(revisions), orient='columns')
    return resp.text
