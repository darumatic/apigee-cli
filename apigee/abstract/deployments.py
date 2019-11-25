#!/usr/bin/env python
"""https://apidocs.apigee.com/api/deployments"""

import json
from abc import ABC, abstractmethod

import pandas as pd
from pandas.io.json import json_normalize

class IDeployments:

    def __init__(self, args):
        self._args = args

    def __call__(self):
        pass

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @abstractmethod
    def get_api_proxy_deployment_details(self, formatted=False):
        pass

class DeploymentsSerializer:
    def serialize_details(self, deployment_details, format, max_colwidth=40):
        if format == 'text':
            return deployment_details.text
        revisions = []
        for i in deployment_details.json()['environment']:
            revisions.append({
                'name':i['name'],'revision':[
                    j['name'] for j in i['revision']
                ]
            })
        if format == 'json':
            return json.dumps(revisions)
        elif format == 'table':
            pd.set_option('display.max_colwidth', max_colwidth)
            return pd.DataFrame.from_dict(json_normalize(revisions), orient='columns')
        # else:
        #     raise ValueError(format)
        return deployment_details
