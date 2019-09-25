import base64
import configparser
import os
import time

import jwt

from apigee import *
from apigee.api.developers import Developers
from apigee.util import mfa_with_pyotp
from apigee.util.os import makedirs


def set_header(hdrs, args):
    if hdrs is None:
        hdrs = {}
    if args.mfa_secret:
        access_token = ""
        makedirs(APIGEE_CLI_DIRECTORY)
        try:
            with open(APIGEE_CLI_ACCESS_TOKEN_FILE, "r") as f:
                access_token = f.read()
        except (IOError, OSError) as e:
            pass
        finally:
            if access_token:
                decoded = jwt.decode(access_token, verify=False)
                if (
                    decoded["exp"] < int(time.time())
                    or decoded["email"] != args.username
                ):
                    access_token = ""
        if not access_token:
            access_token = mfa_with_pyotp.get_access_token(args)
            with open(APIGEE_CLI_ACCESS_TOKEN_FILE, "w") as f:
                f.write(access_token)
        hdrs["Authorization"] = f"Bearer {access_token}"
    else:
        cred = base64.b64encode((f"{args.username}:{args.password}").encode()).decode()
        hdrs["Authorization"] = f"Basic {cred}"
    return hdrs


def get_credential(section, key):
    try:
        config = configparser.ConfigParser()
        config.read(APIGEE_CLI_CREDENTIALS_FILE)
        if section in config:
            return config[section][key]
    except:
        return


def with_prefix(
    name, args, attribute_name=APIGEE_CLI_AUTHORIZATION_DEVELOPER_ATTRIBUTE
):
    team = (
        Developers(args, args.org, args.username)
        .get_developer_attribute(attribute_name)
        .json()["value"]
    )
    allowed = team.split(",")
    for prefix in allowed:
        if name.startswith(prefix):
            return name
    raise Exception(
        f"401 Client Error: Unauthorized for team: {str(allowed)}\nAttempted to access resource: {name}"
    )
