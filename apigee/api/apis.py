#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/api-proxies"""

import json
import os
import requests
import sys
import xml.etree.ElementTree as et
import zipfile
from pathlib import Path

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.apis import IApis, ApisSerializer, IPull
from apigee.api.deployments import Deployments
from apigee.api.keyvaluemaps import Keyvaluemaps
from apigee.api.targetservers import Targetservers
from apigee.util import authorization
from apigee.util.os import (makedirs, path_exists, paths_exist,
                            extractzip, writezip, splitpath)

class Apis(IApis):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def delete_api_proxy_revision(self, revision_number):
        uri = '{0}/v1/organizations/{1}/apis/{2}/revisions/{3}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name,
                    revision_number)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def gen_deployment_detail(self, deployment):
        return {
            'name':deployment['name'],'revision':[
                revision['name'] for revision in deployment['revision']
            ]
        }

    def delete_revisions(self, revision_number):
        print('Deleting revison', revision_number)
        self.delete_api_proxy_revision(revision_number)

    def delete_undeployed_revisions(self, save_last=0, dry_run=False):
        # get all revisions
        revisions = self.list_api_proxy_revisions().json()
        # get deployment details
        deployments = Deployments(self._auth, self._org_name, self._api_name) \
            .get_api_proxy_deployment_details().json()['environment']
        deployment_details = list(map(self.gen_deployment_detail, deployments))
        # filter deployment details to get deployed revisions
        deployed = []
        list(map(lambda dep: deployed.extend(dep['revision']), deployment_details))
        deployed = list(set(deployed))
        # get undeployed revisions by comparing all revisions with deployed revisions
        undeployed = [int(rev) for rev in revisions if rev not in deployed]
        undeployed.sort()
        undeployed_length = len(undeployed)
        undeployed = undeployed[:undeployed_length - (save_last if save_last <= undeployed_length else undeployed_length)]
        print('Undeployed revisions:', undeployed)
        # delete undeployed revisions
        list(map(self.delete_revisions, undeployed)) if not dry_run else None

    def export_api_proxy(self, revision_number, write=True, output_file=None):
        uri = '{0}/v1/organizations/{1}/apis/{2}/revisions/{3}?format=bundle' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name,
                    revision_number)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        if write: writezip(output_file, resp.content)
        return resp

    def get_api_proxy(self):
        uri = '{0}/v1/organizations/{1}/apis/{2}' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp

    def list_api_proxies(self, prefix=None):
        uri = '{0}/v1/organizations/{1}/apis' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return ApisSerializer().serialize_details(resp, 'json', prefix=prefix)

    def list_api_proxy_revisions(self):
        uri = '{0}/v1/organizations/{1}/apis/{2}/revisions' \
            .format(APIGEE_ADMIN_API_URL,
                    self._org_name,
                    self._api_name)
        hdrs = authorization.set_header({'Accept': 'application/json'},
                                        self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # print(resp.status_code)
        return resp
