#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/data-masks"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def create_data_masks_for_an_api_proxy(args):
    uri = '{}/v1/organizations/{}/apis/{}/maskconfigs'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = json.loads(args.body)
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def delete_data_masks_for_an_api_proxy(args):
    uri = '{}/v1/organizations/{}/apis/{}/maskconfigs/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name, args.maskconfig_name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.delete(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def get_data_mask_details_for_an_api_proxy(args):
    uri = '{}/v1/organizations/{}/apis/{}/maskconfigs/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name, args.maskconfig_name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def list_data_masks_for_an_api_proxy(args):
    uri = '{}/v1/organizations/{}/apis/{}/maskconfigs'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def list_data_masks_for_an_organization(args):
    uri = '{}/v1/organizations/{}/maskconfigs'.format(
        APIGEE_ADMIN_API_URL, args.org)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp
