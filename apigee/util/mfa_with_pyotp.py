import binascii
import pyotp
import requests
import sys
import urllib.request, urllib.parse, urllib.error
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

from apigee import APIGEE_ADMIN_API_URL
from apigee import APIGEE_CLI_SUPPRESS_RETRY_MESSAGE
from apigee import APIGEE_CLI_SUPPRESS_RETRY_RESPONSE
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
    postHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Accept':'application/json;charset=utf-8',
        'Authorization':'Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0'
    }
    postBody = 'username=' + urllib.parse.quote(APIGEE_USERNAME) + '&password=' + urllib.parse.quote(APIGEE_PASSWORD) + '&grant_type=password'
    try:
        responsePost = session.post(APIGEE_OAUTH_URL + '?mfa_token=' + TOTP.now(), headers=postHeaders, data=postBody)
    except ConnectionError as ce:
        console.log(ce)
    try:
        responsePost.json()['access_token']
    except KeyError as ke:
        if APIGEE_CLI_SUPPRESS_RETRY_MESSAGE not in (True, 'True', 'true', '1'):
            console.log('retry http POST ' + APIGEE_OAUTH_URL)
        responsePost = session.post(APIGEE_OAUTH_URL + '?mfa_token=' + TOTP.now(), headers=postHeaders, data=postBody)
        if APIGEE_CLI_SUPPRESS_RETRY_RESPONSE not in (True, 'True', 'true', '1'):
            console.log(responsePost.json())
    return responsePost.json()['access_token']
