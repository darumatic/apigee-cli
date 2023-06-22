import base64
import binascii
import configparser
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

import click
import contextlib
import jwt
import pyotp
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

from apigee import (APIGEE_CLI_ACCESS_TOKEN_FILE, APIGEE_CLI_CREDENTIALS_FILE,
                    APIGEE_CLI_DIRECTORY, APIGEE_CLI_IS_MACHINE_USER,
                    APIGEE_OAUTH_URL, APIGEE_SAML_LOGIN_URL,
                    APIGEE_ZONENAME_OAUTH_URL, console,
                    APIGEE_CLI_REFRESH_TOKEN_FILE)
from apigee.cls import AliasedGroup
from apigee.silent import common_silent_options
from apigee.types import Struct
from apigee.utils import create_directory
from apigee.verbose import common_verbose_options


def attach_is_token_option(func, profile):
    is_token = get_config_value(profile, "is_token")
    is_token_envvar = os.environ.get("APIGEE_IS_TOKEN", "")
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


def attach_mfa_secret_option(func, profile):
    mfa_secret = get_config_value(profile, "mfa_secret")
    mfa_envvar = os.environ.get("APIGEE_MFA_SECRET", "")
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


def attach_org_option(func, profile):
    org = get_config_value(profile, "org")
    org_envvar = os.environ.get("APIGEE_ORG", "")
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


def attach_password_option(func, profile):
    password = get_config_value(profile, "password")
    password_envvar = os.environ.get("APIGEE_PASSWORD", "")
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


def attach_username_option(func, profile):
    username = get_config_value(profile, "username")
    username_envvar = os.environ.get("APIGEE_USERNAME", "")
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


def attach_zonename_option(func, profile):
    zonename = get_config_value(profile, "zonename")
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


def common_auth_options(func):
    profile = "default"
    for i, arg in enumerate(sys.argv):
        if arg in ["-P", "--profile"]:
            with contextlib.suppress(IndexError):
                profile = sys.argv[i + 1]
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


def generate_authentication(username=None, password=None, mfa_secret=None, token=None, zonename=None):
    return Struct(
        username=username,
        password=password,
        mfa_secret=mfa_secret,
        token=token,
        zonename=zonename,
    )


def generate_authentication_error_message(authentication_error):
    error_message = f"An exception of type {type(authentication_error).__name__} occurred. Arguments:\n{authentication_error}\nDouble check your credentials and try again."
    return (
        f"{error_message} \nWARNING: APIGEE_CLI_IS_MACHINE_USER={APIGEE_CLI_IS_MACHINE_USER}"
        if APIGEE_CLI_IS_MACHINE_USER
        else error_message
    )


def get_access_token_for_token(
    auth, username, password, oauth_url, post_headers, session
):
    if auth.zonename:
        oauth_url = APIGEE_ZONENAME_OAUTH_URL.format(zonename=auth.zonename)
    post_body = f"username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}&grant_type=password&response_type=token"
    try:
        response_post = session.post(f"{oauth_url}", headers=post_headers, data=post_body)
        return response_post.json()
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
        response_data = response_post.json()
        response_data["access_token"]
        return response_post
    except KeyError:
        return session.post(
            f"{oauth_url}?mfa_token={totp.now()}", headers=post_headers, data=post_body
        )


def get_access_token(auth, username, password, oauth_url, post_headers, session):
    if auth.token or APIGEE_CLI_IS_MACHINE_USER:
        return get_access_token_for_token(auth, username, password, oauth_url, post_headers, session)
    elif auth.mfa_secret:
        return get_access_token_for_mfa(auth, username, password, oauth_url, post_headers, session)
    elif auth.zonename:
        return get_access_token_for_sso(auth, username, password, oauth_url, post_headers, session)


def get_access_token_for_sso(
    auth, username, password, oauth_url, post_headers, session
):
    refresh_token = validate_refresh_token(auth)
    oauth_url = APIGEE_ZONENAME_OAUTH_URL.format(zonename=auth.zonename)
    passcode_url = APIGEE_SAML_LOGIN_URL.format(zonename=auth.zonename)
    if not refresh_token:
        post_body = get_sso_access_token_parameters(passcode_url)
    else:
        # Should we notify users that the refresh token is being used to verify the access token?
        #console.echo("Refresh Token found, renewing access token with Refresh Token...")
        post_body = f"grant_type=refresh_token&refresh_token={refresh_token}"

    try:
        try:
            response_post = session.post(
                f"{oauth_url}", headers=post_headers, data=post_body
            )
            response_data = response_post.json()
            response_data["access_token"]
            # If we didn't have a refresh token previously, save the refresh token we just got.
            if not refresh_token:
                with open(APIGEE_CLI_REFRESH_TOKEN_FILE, "w") as f:
                    f.write(response_data["refresh_token"])
            return response_data
        except KeyError:
            sys.exit("Temporary Authentication Code or Refresh Token is invalid. Please try again.")
    except ConnectionError as ce:
        console.echo(ce)
    except KeyError:
        pass


def get_config_value(config_section, config_key):
    try:
        config = configparser.ConfigParser()
        config.read(APIGEE_CLI_CREDENTIALS_FILE)
        if config_section in config:
            return config[config_section][config_key]
    except Exception:
        return


def get_sso_access_token_parameters(passcode_url):
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

    passcode = click.prompt("Please enter the Temporary Authentication Code")
    return f"passcode={passcode}&grant_type=password&response_type=token"


def retrieve_access_token(authentication, session=None):
    oauth_url = APIGEE_OAUTH_URL
    username = authentication.username
    password = authentication.password
    adapter = HTTPAdapter()
    session = requests.Session()
    session.mount("https://", adapter)
    post_headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Accept": "application/json;charset=utf-8",
        "Authorization": "Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0",
    }
    response_data = get_access_token(authentication, username, password, oauth_url, post_headers, session)
    try:
        return response_data["access_token"]
    except KeyError as error:
        sys.exit(generate_authentication_error_message(error))


def set_authentication_headers(authentication_object, custom_headers=None):
    if custom_headers is None:
        custom_headers = {}
    if authentication_object.mfa_secret or authentication_object.token or authentication_object.zonename:
        access_token = validate_access_token(authentication_object)
        if not access_token:
            access_token = retrieve_access_token(authentication_object)
            with open(APIGEE_CLI_ACCESS_TOKEN_FILE, "w") as f:
                f.write(access_token)
        custom_headers["Authorization"] = f"Bearer {access_token}"
    else:
        custom_headers["Authorization"] = (
            "Basic "
            + base64.b64encode(
                (f"{authentication_object.username}:{authentication_object.password}").encode()
            ).decode()
        )
    return custom_headers


def validate_access_token(authentication_object):
    return validate_jwt_token(authentication_object, APIGEE_CLI_ACCESS_TOKEN_FILE, "email")

def validate_refresh_token(authentication_object):
    return validate_jwt_token(authentication_object, APIGEE_CLI_REFRESH_TOKEN_FILE, "user_name")

def validate_jwt_token(authentication_object, file_name, username_field):
    jwt_token = ""
    create_directory(APIGEE_CLI_DIRECTORY)
    with contextlib.suppress(IOError, OSError):
        with open(file_name, "r") as f:
            jwt_token = f.read().strip()
    if jwt_token:
        decoded = jwt.decode(
            jwt_token,
            options={
                "verify_exp": False,
                "verify_signature": False,
                "verify_aud": False,
            },
        )
        if (
            decoded["exp"] < int(time.time())
            or decoded[username_field].lower() != authentication_object.username.lower()
        ):
            jwt_token = ""
    return jwt_token


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
        retrieve_access_token(generate_authentication(username, password, mfa_secret, token, zonename))
    )


@auth.command(help="view the current access token")
@common_auth_options
@common_verbose_options
@common_silent_options
def view_access_token(
    username, password, mfa_secret, token, zonename, org, profile, **kwargs
):
    authentication_object = generate_authentication(username, password, mfa_secret, token, zonename)
    if authentication_object.mfa_secret or authentication_object.token or authentication_object.zonename:
        # Update token if needed and show it
        set_authentication_headers(authentication_object)
        console.echo(validate_access_token(authentication_object))
    else:
        # Show the user/password base64 basic auth value
        console.echo(
            base64.b64encode(
                f"{authentication_object.username}:{authentication_object.password}".encode()
            ).decode()
        )


@auth.command(help="Clear cached access token and refresh token")
@common_verbose_options
@common_silent_options
def clear(
    **kwargs
):
    if os.path.isfile(APIGEE_CLI_ACCESS_TOKEN_FILE):
        os.remove(APIGEE_CLI_ACCESS_TOKEN_FILE)
        console.echo(f"Removed access token file ({APIGEE_CLI_ACCESS_TOKEN_FILE})")
    else:
        console.echo(f"Access token file not found ({APIGEE_CLI_ACCESS_TOKEN_FILE})")

    if os.path.isfile(APIGEE_CLI_REFRESH_TOKEN_FILE):
        os.remove(APIGEE_CLI_REFRESH_TOKEN_FILE)
        console.echo(f"Removed refresh token file ({APIGEE_CLI_REFRESH_TOKEN_FILE})")
    else:
        console.echo(f"Refresh token file not found ({APIGEE_CLI_REFRESH_TOKEN_FILE})")

