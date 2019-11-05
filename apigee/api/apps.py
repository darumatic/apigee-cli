#!/usr/bin/env python
"""https://apidocs.apigee.com/api/apps-developer"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def create_developer_app(args):
    uri = '{}/v1/organizations/{}/developers/{}/apps'.format(
        APIGEE_ADMIN_API_URL, args.org, args.developer)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = json.loads(args.body)
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def create_empty_developer_app(args):
    uri = '{}/v1/organizations/{}/developers/{}/apps'.format(
        APIGEE_ADMIN_API_URL, args.org, args.developer)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = {
     "name" : args.name,
     # "apiProducts": args.products,
     "attributes" : [
      {
       "name" : "DisplayName",
       "value" : args.display_name
      }
     ],
     # "scopes" : args.scopes,
     "callbackUrl" : args.callback_url
    }
    if not args.display_name:
        del body['attributes']
    if not args.callback_url:
        del body['callback_url']
    # body = {k: v for k, v in body.items() if v}
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    args.consumer_key = resp.json()['credentials'][0]['consumerKey']
    delete_key_for_a_developer_app(args)
    return get_developer_app_details(args)

def get_developer_app_details(args):
    uri = '{}/v1/organizations/{}/developers/{}/apps/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.developer, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def list_developer_apps(args):
    if args.expand:
        uri = '{}/v1/organizations/{}/developers/{}/apps?expand={}'.format(
            APIGEE_ADMIN_API_URL, args.org, args.developer, args.expand)
    else:
        uri = '{}/v1/organizations/{}/developers/{}/apps?count={}&startKey={}'.format(
            APIGEE_ADMIN_API_URL, args.org, args.developer, args.count, args.startkey)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.prefix:
        return json.dumps([i for i in resp.json() if i.startswith(args.prefix)])
    return resp.text

def delete_key_for_a_developer_app(args):
    uri = '{}/v1/organizations/{}/developers/{}/apps/{}/keys/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.developer, args.name, args.consumer_key)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.delete(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp
