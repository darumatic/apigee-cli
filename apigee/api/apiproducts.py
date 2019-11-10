#!/usr/bin/env python
"""https://apidocs.apigee.com/api/api-products-1"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def create_api_product(args):
    uri = '{}/v1/organizations/{}/apiproducts'.format(
        APIGEE_ADMIN_API_URL, args.org)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = json.loads(args.body)
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def delete_api_product(args):
    uri = '{}/v1/organizations/{}/apiproducts/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.delete(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def get_api_product(args):
    uri = '{}/v1/organizations/{}/apiproducts/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def list_api_products(args):
    uri = '{}/v1/organizations/{}/apiproducts?expand={}&count={}&startKey={}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.expand, args.count, args.startkey)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.prefix:
        return json.dumps([i for i in resp.json() if i.startswith(args.prefix)])
    return resp.text

def update_api_product(args):
    uri = '{}/v1/organizations/{}/apiproducts/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = json.loads(args.body)
    resp = requests.put(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def push_apiproducts(args):
    with open(args.file) as file:
        body = file.read()
    apiproduct = json.loads(body)

    args.name = apiproduct['name']
    args.body = body

    try:
        get_api_product(args)
        print('Updating', args.name)
        print(update_api_product(args).text)
    except requests.exceptions.HTTPError:
        print('Creating', args.name)
        print(create_api_product(args).text)
