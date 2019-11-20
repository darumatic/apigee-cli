#!/usr/bin/env python
"""https://apidocs.apigee.com/api/deployments"""

import json
import requests

import pandas as pd
from pandas.io.json import json_normalize

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.deployments import IDeployments
from apigee.util import authorization

class Deployments(IDeployments):

    def __init__(self, args, **kwargs):
        super().__init__(args, **kwargs)

    def get_api_proxy_deployment_details(self):
        args = self._args
        uri = '{}/v1/organizations/{}/apis/{}/deployments'.format(
            APIGEE_ADMIN_API_URL, args.org, args.name)
        hdrs = authorization.set_header({'Accept': 'application/json'}, args)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        if self._isformat:
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
        return resp
