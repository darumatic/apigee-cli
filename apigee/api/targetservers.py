#!/usr/bin/env python
"""https://apidocs.apigee.com/api/api_resources/51-targetservers"""

import requests
import json

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def create_a_targetserver(args):
    uri = '{}/v1/organizations/{}/environments/{}/targetservers'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = json.loads(args.body)
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def delete_a_targetserver(args):
    uri = '{}/v1/organizations/{}/environments/{}/targetservers/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.delete(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def list_targetservers_in_an_environment(args):
    uri = '{}/v1/organizations/{}/environments/{}/targetservers'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.prefix:
        return json.dumps([i for i in resp.json() if i.startswith(args.prefix)])
    return resp.text

def get_targetserver(args):
    uri = '{}/v1/organizations/{}/environments/{}/targetservers/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def update_a_targetserver(args):
    uri = '{}/v1/organizations/{}/environments/{}/targetservers/{}'.format(
        APIGEE_ADMIN_API_URL, args.org, args.environment, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = json.loads(args.body)
    resp = requests.put(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def push_targetserver(args):
    with open(args.file) as file:
        body = file.read()
    targetserver = json.loads(body)

    args.name = targetserver['name']
    args.body = body

    try:
        get_targetserver(args)
        print('Updating', args.name)
        print(update_a_targetserver(args).text)
    except requests.exceptions.HTTPError:
        print('Creating', args.name)
        print(create_a_targetserver(args).text)
