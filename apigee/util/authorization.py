import configparser
import base64

from apigee import APIGEE_CLI_CREDS
from apigee.util import mfa_with_pyotp

def set_header(hdrs, args):
    if hdrs is None:
        hdrs = dict()
    if args.mfa_secret:
        hdrs['Authorization'] = 'Bearer ' + mfa_with_pyotp.get_access_token(args)
    else:
        hdrs['Authorization'] = 'Basic ' + base64.b64encode((args.username + ':' + args.password).encode()).decode()
    return hdrs

def get_credential(section, key):
    try:
        config = configparser.ConfigParser()
        config.read(APIGEE_CLI_CREDS)
        if section in config:
            return config[section][key]
    except:
        return None
