#!/usr/bin/env python
"""https://apidocs.apigee.com/api-services/content/environment-keyvalue-maps"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def create_keyvaluemap_in_an_environment(args):
    uri = '{}/v1/organizations/{}/environments/{}/keyvaluemaps'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = json.loads(args.body)
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def delete_keyvaluemap_from_an_environment(args):
    uri = '{}/v1/organizations/{}/environments/{}/keyvaluemaps/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.delete(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def delete_keyvaluemap_entry_in_an_environment(args):
    uri = '{}/v1/organizations/{}/environments/{}/keyvaluemaps/{}/entries/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name, args.entry_name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.delete(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def get_keyvaluemap_in_an_environment(args):
    uri = '{}/v1/organizations/{}/environments/{}/keyvaluemaps/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def get_a_keys_value_in_an_environment_scoped_keyvaluemap(args):
    uri = '{}/v1/organizations/{}/environments/{}/keyvaluemaps/{}/entries/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name, args.entry_name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def list_keyvaluemaps_in_an_environment(args):
    uri = '{}/v1/organizations/{}/environments/{}/keyvaluemaps'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.prefix:
        return json.dumps([i for i in resp.json() if i.startswith(args.prefix)])
    return resp.text

def update_keyvaluemap_in_an_environment(args):
    uri = '{}/v1/organizations/{}/environments/{}/keyvaluemaps/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = json.loads(args.body)
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def create_an_entry_in_an_environment_scoped_kvm(args):
    uri = '{}/v1/organizations/{}/environments/{}/keyvaluemaps/{}/entries'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = {
      'name' : args.entry_name,
      'value' : args.entry_value
    }
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def update_an_entry_in_an_environment_scoped_kvm(args):
    uri = '{}/v1/organizations/{}/environments/{}/keyvaluemaps/{}/entries/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name, args.entry_name)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = {
      'name' : args.entry_name,
      'value' : args.updated_value
    }
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def list_keys_in_an_environment_scoped_keyvaluemap(args):
    uri = '{}/v1/organizations/{}/environments/{}/keyvaluemaps/{}/keys?startkey={}&count={}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name, args.startkey, args.count)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.prefix:
        return json.dumps([i for i in resp.json() if i.startswith(args.prefix)])
    return resp.text
