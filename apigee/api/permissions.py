#!/usr/bin/env python
"""https://docs.apigee.com/api-platform/system-administration/permissions"""

import requests
import json

import pandas as pd
from pandas.io.json import json_normalize

from apigee import APIGEE_ADMIN_API_URL
from apigee.util import authorization

def create_permissions(args):
    uri = '{}/v1/organizations/{}/userroles/{}/resourcepermissions'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = json.loads(args.body)
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def team_permissions(args):
    uri = '{}/v1/organizations/{}/userroles/{}/resourcepermissions'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json', 'Content-Type': 'application/json'}, args)
    body = {
      "resourcePermission" : [
     {
        "organization" : args.org,
        "path" : "/",
        "permissions" : [ "get" ]
      }, {
        "organization" : args.org,
        "path" : "/*",
        "permissions" : [ ]
      }, {
        "organization" : args.org,
        "path" : "/environments/*/targetservers",
        "permissions" : [ "get" ]
      }, {
        "organization" : args.org,
        "path" : "/developers",
        "permissions" : [ "get" ]
      }, {
        "organization" : args.org,
        "path" : "/apiproducts",
        "permissions" : [ "get" ]
      }, {
        "organization" : args.org,
        "path" : "/applications",
        "permissions" : [ "get" ]
      }, {
        "organization" : args.org,
        "path" : "/apiproducts/"+args.team+"*",
        "permissions" : [ "put", "get", "delete" ]
      }, {
        "organization" : args.org,
        "path" : "/applications/"+args.team+"*",
        "permissions" : [ "put", "get", "delete" ]
      }, {
        "organization" : args.org,
        "path" : "/developers/*/apps",
        "permissions" : [ "get" ]
      }, {
        "organization" : args.org,
        "path" : "/environments/*/caches",
        "permissions" : [ "get" ]
      }, {
        "organization" : args.org,
        "path" : "/apiproxies/*/maskconfigs",
        "permissions" : [ "get" ]
      }, {
        "organization" : args.org,
        "path" : "/developers/*/apps/"+args.team+"*",
        "permissions" : [ "put", "get", "delete" ]
      }, {
        "organization" : args.org,
        "path" : "/apiproxies/"+args.team+"*/maskconfigs",
        "permissions" : [ "put", "get", "delete" ]
      }, {
        "organization" : args.org,
        "path" : "/environments/*/keyvaluemaps",
        "permissions" : [ "get" ]
      }, {
        "organization" : args.org,
        "path" : "/environments/*/caches/"+args.team+"*",
        "permissions" : [ "put", "get", "delete" ]
      }, {
        "organization" : args.org,
        "path" : "/environments/*/keyvaluemaps/"+args.team+"*",
        "permissions" : [ "put", "get", "delete" ]
      }, {
        "organization" : args.org,
        "path" : "/environments/*/applications/"+args.team+"*/revisions/*/debugsessions",
        "permissions" : [ "put", "get", "delete" ]
      } ]
    }
    resp = requests.post(uri, headers=hdrs, json=body)
    resp.raise_for_status()
    # print(resp.status_code)
    return resp

def get_permissions(args):
    uri = '{}/v1/o/{}/userroles/{}/permissions'.format(
        APIGEE_ADMIN_API_URL, args.org, args.name)
    hdrs = authorization.set_header({'Accept': 'application/json'}, args)
    resp = requests.get(uri, headers=hdrs)
    resp.raise_for_status()
    # print(resp.status_code)
    if args.json:
        return resp.text
    pd.set_option('display.max_colwidth', args.max_colwidth)
    return pd.DataFrame.from_dict(json_normalize(resp.json()['resourcePermission']), orient='columns')
