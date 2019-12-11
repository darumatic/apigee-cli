#!/usr/bin/env python
"""https://apidocs.apigee.com/api/deployments"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.deployments import IDeployments, DeploymentsSerializer
from apigee.util import authorization

class Deployments(IDeployments):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_api_proxy_deployment_details(self, formatted=False, format='text', showindex=False, tablefmt='plain', revision_name_only=False):
        uri = '{0}/v1/organizations/{1}/apis/{2}/deployments' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        if formatted:
            if revision_name_only:
                # return DeploymentsSerializer().serialize_details(resp, 'table', max_colwidth=args.max_colwidth)
                return DeploymentsSerializer().serialize_details(resp, format, showindex=showindex, tablefmt=tablefmt)
            return DeploymentsSerializer().serialize_details(resp, 'text')
        return resp
