#!/usr/bin/env python
"""https://apidocs.apigee.com/api/apps-developer

https://apidocs.apigee.com/api/developer-app-keys
"""

import random
import requests
import json
import string

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
    uri = '{}/v1/organizations/{}/developers/{}/apps'.format(
        APIGEE_ADMIN_API_URL, args.org, args.developer)
    if args.expand:
        uri += '?expand={}'.format(args.expand)
    else:
        uri += '?count={}&startKey={}'.format(args.count, args.startkey)
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

def create_a_consumer_key_and_secret(args):
    uri = '{}/v1/organizations/{}/developers/{}/apps/{}/keys/create'.format(
        APIGEE_ADMIN_API_URL, args.org, args.developer, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    app = get_developer_app_details(args)
    if not args.consumer_key:
        args.consumer_key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(args.key_length))
    if not args.consumer_secret:
        args.consumer_secret = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(args.secret_length))
    if args.key_suffix:
        args.consumer_key += args.key_delimiter
        args.consumer_key += args.key_suffix
    body = {
      "consumerKey": args.consumer_key,
      "consumerSecret": args.consumer_secret
    }
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.products:
        print(resp.text)
        args.consumer_key = resp.json()['consumerKey']
        args.body = json.dumps({ "apiProducts": args.products,
          "attributes": resp.json()['attributes']
        })
        print('Adding API Products', args.products, 'to consumerKey', args.consumer_key)
        return add_api_product_to_key(args)
    return resp

def add_api_product_to_key(args):
    uri = '{}/v1/organizations/{}/developers/{}/apps/{}/keys/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.developer, args.name, args.consumer_key)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = json.loads(args.body)
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp
