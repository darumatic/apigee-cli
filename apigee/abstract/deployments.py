#!/usr/bin/env python
"""https://apidocs.apigee.com/api/deployments"""

import json
from abc import ABC, abstractmethod

# import pandas as pd
# from pandas.io.json import json_normalize
from tabulate import tabulate

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
    def get_api_proxy_deployment_details(self, formatted=False, showindex=False, tablefmt='plain'):
        pass

class DeploymentsSerializer:
    def serialize_details(self, deployment_details, format, showindex=False, tablefmt='plain'):
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
        elif format == 'table': #max_colwidth=40
            # pd.set_option('display.max_colwidth', max_colwidth)
            # return pd.DataFrame.from_dict(json_normalize(revisions), orient='columns')
            table = [[rev['name'], rev['revision']] for rev in revisions]
            headers = list()
            if showindex == 'always' or showindex is True:
                headers = ['id', 'name', 'revision']
            elif showindex == 'never' or showindex is False:
                headers = ['name', 'revision']
            return tabulate(table, headers, showindex=showindex, tablefmt=tablefmt)
        # else:
        #     raise ValueError(format)
        return deployment_details
