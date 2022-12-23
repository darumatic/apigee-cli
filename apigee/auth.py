import base64
import binascii
import configparser
import inspect
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

import click
import jwt
import pyotp
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from requests.packages.urllib3.util.retry import Retry

from apigee import (
    APIGEE_CLI_ACCESS_TOKEN_FILE,
    APIGEE_CLI_CREDENTIALS_FILE,
    APIGEE_CLI_DIRECTORY,
    APIGEE_CLI_IS_MACHINE_USER,
    APIGEE_OAUTH_URL,
    APIGEE_SAML_LOGIN_URL,
    APIGEE_ZONENAME_OAUTH_URL,
    console,
)
from apigee.cls import AliasedGroup

# from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.types import Struct
from apigee.utils import make_dirs
from apigee.verbose import common_verbose_options


def attach_username_option(func, profile):
    username = get_credential(profile, "username")
    username_envvar = os.environ.get(f"APIGEE_USERNAME", "")
    if username:
        func = click.option(
            "-u", "--username", default=username, show_default="current username"
        )(func)
    elif username_envvar:
        func = click.option(
            "-u", "--username", default=username_envvar, show_default="current username"
        )(func)
    else:
        func = click.option("-u", "--username", required=True)(func)
    return func


def attach_password_option(func, profile):
    password = get_credential(profile, "password")
    password_envvar = os.environ.get(f"APIGEE_PASSWORD", "")
    if password:
        func = click.option(
            "-p", "--password", default=password, show_default="current password"
        )(func)
    elif password_envvar:
        func = click.option(
            "-p", "--password", default=password_envvar, show_default="current password"
        )(func)
    else:
        func = click.option("-p", "--password", required=True)(func)
    return func


def attach_mfa_secret_option(func, profile):
    mfa_secret = get_credential(profile, "mfa_secret")
    mfa_envvar = os.environ.get(f"APIGEE_MFA_SECRET", "")
    if mfa_secret:
        func = click.option(
            "-mfa", "--mfa-secret", default=mfa_secret, show_default="current mfa key"
        )(func)
    elif mfa_envvar:
        func = click.option(
            "-mfa", "--mfa-secret", default=mfa_envvar, show_default="current mfa key"
        )(func)
    else:
        func = click.option("-mfa", "--mfa-secret")(func)
    return func


def attach_is_token_option(func, profile):
    is_token = get_credential(profile, "is_token")
    is_token_envvar = os.environ.get(f"APIGEE_IS_TOKEN", "")
    if is_token in (True, "True", "true", "1"):
        func = click.option(
            "--token/--no-token",
            default=is_token,
            show_default=True,
            help="specify to use oauth without MFA",
        )(func)
    elif is_token_envvar in (True, "True", "true", "1"):
        func = click.option(
            "--token/--no-token",
            default=is_token_envvar,
            show_default=True,
            help="specify to use oauth without MFA",
        )(func)
    else:
        func = click.option(
            "--token/--no-token",
            default=False,
            show_default=True,
            help="specify to use oauth without MFA",
        )(func)
    return func


def attach_zonename_option(func, profile):
    zonename = get_credential(profile, "zonename")
    zonename_envvar = os.environ.get("APIGEE_ZONENAME", "")
    if zonename:
        func = click.option(
            "-z",
            "--zonename",
            default=zonename,
            show_default="current identity zone name",
        )(func)
    elif zonename_envvar:
        func = click.option(
            "-z",
            "--zonename",
            default=zonename_envvar,
            show_default="current identity zone name",
        )(func)
    else:
        func = click.option("-z", "--zonename", help="identity zone name")(func)
    return func


def attach_org_option(func, profile):
    org = get_credential(profile, "org")
    org_envvar = os.environ.get(f"APIGEE_ORG", "")
    if org:
        func = click.option("-o", "--org", default=org, show_default="current org")(
            func
        )
    elif org_envvar:
        func = click.option(
            "-o", "--org", default=org_envvar, show_default="current org"
        )(func)
    else:
        func = click.option("-o", "--org", required=True)(func)
    return func


def common_auth_options(func):
    profile = "default"
    for i, arg in enumerate(sys.argv):
        if arg == "-P" or arg == "--profile":
            try:
                profile = sys.argv[i + 1]
            except IndexError:
                pass
    attach_username_option(func, profile)
    attach_password_option(func, profile)
    attach_mfa_secret_option(func, profile)
    attach_is_token_option(func, profile)
    attach_zonename_option(func, profile)
    attach_org_option(func, profile)
    func = click.option(
        "-P",
        "--profile",
        help="name of the user profile to authenticate with",
        default=profile,
        show_default=True,
    )(func)
    return func


def check_access_token(auth_obj):
    access_token = ""
    make_dirs(APIGEE_CLI_DIRECTORY)
    try:
        with open(APIGEE_CLI_ACCESS_TOKEN_FILE, "r") as f:
            access_token = f.read().strip()
    except (IOError, OSError):
        pass

    if access_token:
        decoded = jwt.decode(
            access_token,
            options={
                "verify_exp": False,
                "verify_signature": False,
                "verify_aud": False,
            },
        )
        if (
            decoded["exp"] < int(time.time())
            or decoded["email"].lower() != auth_obj.username.lower()
        ):
            access_token = ""
    return access_token


def gen_auth(username=None, password=None, mfa_secret=None, token=None, zonename=None):
    return Struct(
        username=username,
        password=password,
        mfa_secret=mfa_secret,
        token=token,
        zonename=zonename,
    )


def get_access_token_for_token(
    auth, username, password, oauth_url, post_headers, session
):
    if auth.zonename:
        oauth_url = APIGEE_ZONENAME_OAUTH_URL.format(zonename=auth.zonename)
    post_body = f"username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}&grant_type=password&response_type=token"
    try:
        return session.post(f"{oauth_url}", headers=post_headers, data=post_body)
    except ConnectionError as ce:
        console.echo(ce)


def get_access_token_for_mfa(
    auth, username, password, oauth_url, post_headers, session
):
    mfa_secret = auth.mfa_secret
    totp = pyotp.TOTP(mfa_secret)
    try:
        totp.now()
    except binascii.Error as e:
        sys.exit(f"{type(e).__name__}: {e}: Not a valid MFA key")
    post_body = f"username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}&grant_type=password"
    try:
        response_post = session.post(
            f"{oauth_url}?mfa_token={totp.now()}", headers=post_headers, data=post_body
        )
    except ConnectionError as ce:
        console.echo(ce)
    try:
        response_post.json()["access_token"]
        return response_post
    except KeyError:
        return session.post(
            f"{oauth_url}?mfa_token={totp.now()}", headers=post_headers, data=post_body
        )


def get_access_token_for_sso(
    auth, username, password, oauth_url, post_headers, session
):
    oauth_url = APIGEE_ZONENAME_OAUTH_URL.format(zonename=auth.zonename)
    passcode_url = APIGEE_SAML_LOGIN_URL.format(zonename=auth.zonename)
    webbrowser.open(passcode_url)
    console.echo(
        "SSO authorization page has automatically been opened in your default browser."
    )
    console.echo(
        "Follow the instructions in the browser to complete this authorization request."
    )
    console.echo(
        f"""\nIf your browser did not automatically open, go to the following URL and sign in:\n\n{passcode_url}\n\nthen copy the Temporary Authentication Code.\n"""
    )
    try:
        passcode = click.prompt("Please enter the Temporary Authentication Code")
        post_body = f"passcode={passcode}&grant_type=password&response_type=token"
        try:
            response_post = session.post(
                f"{oauth_url}", headers=post_headers, data=post_body
            )
            response_post.json()["access_token"]
            return response_post
        except KeyError:
            sys.exit("Temporary Authentication Code is invalid. Please try again.")
    except ConnectionError as ce:
        console.echo(ce)
    except KeyError:
        pass


def build_auth_error_message(error):
    error_message = f"An exception of type {type(error).__name__} occurred. Arguments:\n{error}\nDouble check your credentials and try again."
    if APIGEE_CLI_IS_MACHINE_USER:
        return f"{error_message} \nWARNING: APIGEE_CLI_IS_MACHINE_USER={APIGEE_CLI_IS_MACHINE_USER}"
    return error_message


def get_access_token(
    auth, retries=4, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None
):
    oauth_url = APIGEE_OAUTH_URL
    username = auth.username
    password = auth.password
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    post_headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Accept": "application/json;charset=utf-8",
        "Authorization": "Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0",
    }
    if auth.token or APIGEE_CLI_IS_MACHINE_USER:
        response_post = get_access_token_for_token(
            auth, username, password, oauth_url, post_headers, session
        )
    elif auth.mfa_secret:
        response_post = get_access_token_for_mfa(
            auth, username, password, oauth_url, post_headers, session
        )
    elif auth.zonename:
        response_post = get_access_token_for_sso(
            auth, username, password, oauth_url, post_headers, session
        )
    else:
        return
    try:
        return response_post.json()["access_token"]
    except KeyError as ke:
        sys.exit(build_auth_error_message(ke))


def get_credential(section, key):
    try:
        config = configparser.ConfigParser()
        config.read(APIGEE_CLI_CREDENTIALS_FILE)
        if section in config:
            return config[section][key]
    except:
        return


def set_header(auth_obj, headers={}):
    if auth_obj.mfa_secret or auth_obj.token or auth_obj.zonename:
        access_token = check_access_token(auth_obj)
        if not access_token:
            access_token = get_access_token(auth_obj)
            with open(APIGEE_CLI_ACCESS_TOKEN_FILE, "w") as f:
                f.write(access_token)
        headers["Authorization"] = f"Bearer {access_token}"
    else:
        headers["Authorization"] = (
            "Basic "
            + base64.b64encode(
                (f"{auth_obj.username}:{auth_obj.password}").encode()
            ).decode()
        )
    return headers


@click.command(
    help="Custom authorization commands. More information on the use cases for these commands are yet to be documented.",
    cls=AliasedGroup,
)
def auth():
    pass


@auth.command(name="get-access-token", help="request a fresh access token")
@common_auth_options
@common_verbose_options
@common_silent_options
def get_access_token_command(
    username, password, mfa_secret, token, zonename, org, profile, **kwargs
):
    console.echo(
        get_access_token(gen_auth(username, password, mfa_secret, token, zonename))
    )


@auth.command(help="view the current access token")
@common_auth_options
@common_verbose_options
@common_silent_options
def view_access_token(
    username, password, mfa_secret, token, zonename, org, profile, **kwargs
):
    auth_obj = gen_auth(username, password, mfa_secret, token, zonename)
    if auth_obj.mfa_secret or auth_obj.token or auth_obj.zonename:
        # Update token if needed and show it
        set_header(auth_obj)
        console.echo(check_access_token(auth_obj))
    else:
        # Show the user/password base64 basic auth value
        console.echo(
            base64.b64encode(
                f"{auth_obj.username}:{auth_obj.password}".encode()
            ).decode()
        )
