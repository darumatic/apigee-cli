import pyotp
import requests
import urllib.request, urllib.parse, urllib.error
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

from apigee import APIGEE_ADMIN_API_URL
from apigee import APIGEE_OAUTH_URL
from apigee import HTTP_MAX_RETRIES

def get_access_token(args):
    if args.mfa_secret is None:
        return None
    APIGEE_USERNAME = args.username
    APIGEE_PASSWORD = args.password
    APIGEE_MFA_SECRET = args.mfa_secret
    TOTP = pyotp.TOTP(APIGEE_MFA_SECRET)
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
        print(ce)
    try:
        responsePost.json()['access_token']
    except KeyError as ke:
        print('retry http POST ' + APIGEE_OAUTH_URL)
        responsePost = session.post(APIGEE_OAUTH_URL + '?mfa_token=' + TOTP.now(), headers=postHeaders, data=postBody)
        print(responsePost.json())
    return responsePost.json()['access_token']
