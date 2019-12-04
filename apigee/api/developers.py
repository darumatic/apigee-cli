#!/usr/bin/env python
"""https://apidocs.apigee.com/api/developers-0"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.developers import IDevelopers, DevelopersSerializer
from apigee.util import authorization

class Developers(IDevelopers):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_developers(self, prefix=None, expand=False, count=100, startkey=''):
        uri = '{0}/v1/organizations/{1}/developers?expand={2}&count={3}&startKey={4}'.format(APIGEE_ADMIN_API_URL, self._org_name, expand, count, startkey)
        hdrs = authorization.set_header({'Accept': 'application/json'}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return DevelopersSerializer().serialize_details(resp, 'json', prefix=prefix)
