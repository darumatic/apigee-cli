import binascii
import pyotp
import requests
import sys
import urllib.request, urllib.parse, urllib.error
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

from apigee import *
from apigee import APIGEE_OAUTH_URL
from apigee import HTTP_MAX_RETRIES
from apigee.util import console

def get_access_token(args):
    if args.mfa_secret is None:
        return
    APIGEE_USERNAME = args.username
    APIGEE_PASSWORD = args.password
    APIGEE_MFA_SECRET = args.mfa_secret
    TOTP = pyotp.TOTP(APIGEE_MFA_SECRET)
    try:
        TOTP.now()
    except binascii.Error as e:
        sys.exit(f'{type(e).__name__}: {e}: Not a valid MFA key')
    adapter = HTTPAdapter(max_retries=HTTP_MAX_RETRIES)
    session = requests.Session()
    session.mount('https://', adapter)
    post_headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Accept':'application/json;charset=utf-8',
        'Authorization':'Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0'
    }
    post_body = 'username=' + urllib.parse.quote(APIGEE_USERNAME) + '&password=' + urllib.parse.quote(APIGEE_PASSWORD) + '&grant_type=password'
    try:
        response_post = session.post(APIGEE_OAUTH_URL + '?mfa_token=' + TOTP.now(), headers=post_headers, data=post_body)
    except ConnectionError as ce:
        console.log(ce)
    try:
        response_post.json()['access_token']
    except KeyError as ke:
        if APIGEE_CLI_SUPPRESS_RETRY_MESSAGE not in (True, 'True', 'true', '1'):
            console.log('retry http POST ' + APIGEE_OAUTH_URL)
        response_post = session.post(APIGEE_OAUTH_URL + '?mfa_token=' + TOTP.now(), headers=post_headers, data=post_body)
        if APIGEE_CLI_SUPPRESS_RETRY_RESPONSE not in (True, 'True', 'true', '1'):
            console.log(response_post.json())
    return response_post.json()['access_token']
