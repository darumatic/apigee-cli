#!/usr/bin/env python
"""https://apidocs.apigee.com/api/deployments"""

import json
import requests

import pandas as pd
from pandas.io.json import json_normalize

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.deployments import IDeployments, DeploymentsSerializer
from apigee.util import authorization

class Deployments(IDeployments):

    def __init__(self, args, **kwargs):
        super().__init__(args, **kwargs)

    def get_api_proxy_deployment_details(self):
        args = self._args
        uri = '{}/v1/organizations/{}/apis/{}/deployments'.format(APIGEE_ADMIN_API_URL, args.org, args.name)
        hdrs = authorization.set_header({'Accept': 'application/json'}, args)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        if self._format:
            if args.revision_name:
                if args.json:
                    return DeploymentsSerializer().serialize_details(resp, 'json')
                return DeploymentsSerializer().serialize_details(resp, 'table')
            return DeploymentsSerializer().serialize_details(resp, 'text', max_colwidth=args.max_colwidth)
        return resp
