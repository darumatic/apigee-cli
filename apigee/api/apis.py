#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.apis import IApis, ApisSerializer
from apigee.api.deployments import Deployments
from apigee.util import authorization
from apigee.util.os import writezip as wzip

class Apis(IApis):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def delete_api_proxy_revision(self, revision_number):
        uri = '{0}/v1/organizations/{1}/apis/{2}/revisions/{3}'.format(APIGEE_ADMIN_API_URL, self._org_name, self._api_name, revision_number)
        hdrs = authorization.set_header({'Accept': 'application/json'}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def delete_undeployed_revisions(self, save_last=0, dry_run=False):
        revisions = self.list_api_proxy_revisions().json()
        deployment_details = []
        for i in Deployments(self._auth, self._org_name, self._api_name).get_api_proxy_deployment_details().json()['environment']:
            deployment_details.append({
                'name':i['name'],'revision':[
                    j['name'] for j in i['revision']
                ]
            })
        deployed = []
        for dep in deployment_details:
            deployed.extend(dep['revision'])
        deployed = list(set(deployed))
        undeployed = [rev for rev in revisions if rev not in deployed]
        undeployed = [int(x) for x in undeployed]
        undeployed.sort()
        undeployed = undeployed[:len(undeployed)-save_last]
        print('Undeployed revisions:', undeployed)
        if not dry_run:
            for rev in undeployed:
                revision_number = rev
                print('Deleting revison', rev)
                self.delete_api_proxy_revision(revision_number)

    def export_api_proxy(self, revision_number, writezip=True, output_file=None):
        uri = '{0}/v1/organizations/{1}/apis/{2}/revisions/{3}?format=bundle'.format(APIGEE_ADMIN_API_URL, self._org_name, self._api_name, revision_number)
        hdrs = authorization.set_header({'Accept': 'application/json'}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        if writezip:
            if output_file:
                zip_file = output_file
            else:
                zip_file = self._api_name + '.zip'
            wzip(zip_file, resp.content)
        return resp

    def get_api_proxy(self):
        uri = '{0}/v1/organizations/{1}/apis/{2}'.format(APIGEE_ADMIN_API_URL, self._org_name, self._api_name)
        hdrs = authorization.set_header({'Accept': 'application/json'}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_api_proxies(self, prefix=None):
        uri = '{0}/v1/organizations/{1}/apis'.format(APIGEE_ADMIN_API_URL, self._org_name)
        hdrs = authorization.set_header({'Accept': 'application/json'}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return ApisSerializer().serialize_details(resp, 'json', prefix=prefix)

    def list_api_proxy_revisions(self):
        uri = '{0}/v1/organizations/{1}/apis/{2}/revisions'.format(APIGEE_ADMIN_API_URL, self._org_name, self._api_name)
        hdrs = authorization.set_header({'Accept': 'application/json'}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp
