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

from apigee import (APIGEE_CLI_ACCESS_TOKEN_FILE, APIGEE_CLI_CREDENTIALS_FILE,
                    APIGEE_CLI_DIRECTORY, APIGEE_CLI_IS_MACHINE_USER,
                    APIGEE_OAUTH_URL, APIGEE_SAML_LOGIN_URL,
                    APIGEE_ZONENAME_OAUTH_URL, console)
from apigee.cls import AliasedGroup
# from apigee.prefix import common_prefix_options
from apigee.prefix import auth_with_prefix as with_prefix
from apigee.silent import common_silent_options
from apigee.types import Struct
from apigee.utils import make_dirs
from apigee.verbose import common_verbose_options


def common_auth_options(func):
    profile = 'default'
    for i, arg in enumerate(sys.argv):
        if arg == '-P' or arg == '--profile':
            try:
                profile = sys.argv[i + 1]
            except IndexError:
                pass
    username = get_credential(profile, 'username')
    username_envvar = os.environ.get(f'APIGEE_USERNAME', '')
    password = get_credential(profile, 'password')
    password_envvar = os.environ.get(f'APIGEE_PASSWORD', '')
    mfa_secret = get_credential(profile, 'mfa_secret')
    mfa_envvar = os.environ.get(f'APIGEE_MFA_SECRET', '')
    is_token = get_credential(profile, 'is_token')
    is_token_envvar = os.environ.get(f'APIGEE_IS_TOKEN', '')
    zonename = get_credential(profile, 'zonename')
    zonename_envvar = os.environ.get('APIGEE_ZONENAME', '')
    org = get_credential(profile, 'org')
    org_envvar = os.environ.get(f'APIGEE_ORG', '')
    if username:
        func = click.option(
            '-u', '--username', default=username, show_default='current username'
        )(func)
    elif username_envvar:
        func = click.option(
            '-u', '--username', default=username_envvar, show_default='current username'
        )(func)
    else:
        func = click.option('-u', '--username', required=True)(func)
    if password:
        func = click.option(
            '-p', '--password', default=password, show_default='current password'
        )(func)
    elif password_envvar:
        func = click.option(
            '-p', '--password', default=password_envvar, show_default='current password'
        )(func)
    else:
        func = click.option('-p', '--password', required=True)(func)
    if mfa_secret:
        func = click.option(
            '-mfa', '--mfa-secret', default=mfa_secret, show_default='current mfa key'
        )(func)
    elif mfa_envvar:
        func = click.option(
            '-mfa', '--mfa-secret', default=mfa_envvar, show_default='current mfa key'
        )(func)
    else:
        func = click.option('-mfa', '--mfa-secret')(func)
    if is_token in (True, 'True', 'true', '1'):
        func = click.option(
            '--token/--no-token',
            default=is_token,
            show_default=True,
            help='specify to use oauth without MFA',
        )(func)
    elif is_token_envvar in (True, 'True', 'true', '1'):
        func = click.option(
            '--token/--no-token',
            default=is_token_envvar,
            show_default=True,
            help='specify to use oauth without MFA',
        )(func)
    else:
        func = click.option(
            '--token/--no-token',
            default=False,
            show_default=True,
            help='specify to use oauth without MFA',
        )(func)
    if zonename:
        func = click.option(
            '-z', '--zonename', default=zonename, show_default='current identity zone name'
        )(func)
    elif zonename_envvar:
        func = click.option(
            '-z',
            '--zonename',
            default=zonename_envvar,
            show_default='current identity zone name',
        )(func)
    else:
        func = click.option('-z', '--zonename', help='identity zone name')(func)
    if org:
        func = click.option('-o', '--org', default=org, show_default='current org')(func)
    elif org_envvar:
        func = click.option('-o', '--org', default=org_envvar, show_default='current org')(
            func
        )
    else:
        func = click.option('-o', '--org', required=True)(func)
    func = click.option(
        '-P',
        '--profile',
        help='name of the user profile to authenticate with',
        default=profile,
        show_default=True,
    )(func)
    return func


def gen_auth(username=None, password=None, mfa_secret=None, token=None, zonename=None):
    return Struct(
        username=username,
        password=password,
        mfa_secret=mfa_secret,
        token=token,
        zonename=zonename,
    )


def get_access_token(
    auth, retries=4, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None
):
    _oauth_url = APIGEE_OAUTH_URL
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
    session.mount('https://', adapter)
    post_headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Accept': 'application/json;charset=utf-8',
        'Authorization': 'Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0',
    }
    _oauth_url = APIGEE_OAUTH_URL
    if auth.token or APIGEE_CLI_IS_MACHINE_USER:
        if auth.zonename:
            _oauth_url = APIGEE_ZONENAME_OAUTH_URL.format(zonename=auth.zonename)
        post_body = f'username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}&grant_type=password&response_type=token'
        try:
            response_post = session.post(f'{_oauth_url}', headers=post_headers, data=post_body)
        except ConnectionError as ce:
            console.echo(ce)
    elif auth.mfa_secret:
        mfa_secret = auth.mfa_secret
        totp = pyotp.TOTP(mfa_secret)
        try:
            totp.now()
        except binascii.Error as e:
            sys.exit(f'{type(e).__name__}: {e}: Not a valid MFA key')
        post_body = f'username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}&grant_type=password'
        try:
            response_post = session.post(
                f'{_oauth_url}?mfa_token={totp.now()}', headers=post_headers, data=post_body
            )
        except ConnectionError as ce:
            console.echo(ce)
        try:
            response_post.json()['access_token']
        except KeyError as ke:
            response_post = session.post(
                f'{_oauth_url}?mfa_token={totp.now()}', headers=post_headers, data=post_body
            )
    elif auth.zonename:
        _oauth_url = APIGEE_ZONENAME_OAUTH_URL.format(zonename=auth.zonename)
        passcode_url = APIGEE_SAML_LOGIN_URL.format(zonename=auth.zonename)
        webbrowser.open(passcode_url)
        console.echo(
            'SSO authorization page has automatically been opened in your default browser.'
        )
        console.echo(
            'Follow the instructions in the browser to complete this authorization request.'
        )
        console.echo(
            f"""\nIf your browser did not automatically open, go to the following URL and sign in:\n\n{passcode_url}\n\nthen copy the Temporary Authentication Code.\n"""
        )
        try:
            passcode = click.prompt('Please enter the Temporary Authentication Code')
            post_body = f'passcode={passcode}&grant_type=password&response_type=token'
            try:
                response_post = session.post(
                    f'{_oauth_url}', headers=post_headers, data=post_body
                )
                response_post.json()['access_token']
            except KeyError:
                sys.exit('Temporary Authentication Code is invalid. Please try again.')
        except ConnectionError as ce:
            console.echo(ce)
        except KeyError:
            pass
    else:
        return
    try:
        return response_post.json()['access_token']
    except KeyError as ke:
        frm = inspect.trace()[-1]
        mod = inspect.getmodule(frm[0])
        modname = mod.__name__ if mod else frm[1]
        if APIGEE_CLI_IS_MACHINE_USER:
            sys.exit(
                f'An exception of type {modname}.{type(ke).__name__} occurred. Arguments:\n{ke}\nDouble check your credentials and try again.\nWARNING: APIGEE_CLI_IS_MACHINE_USER={APIGEE_CLI_IS_MACHINE_USER}'
            )
        sys.exit(
            f'An exception of type {modname}.{type(ke).__name__} occurred. Arguments:\n{ke}\nDouble check your credentials and try again.'
        )


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
        access_token = ""
        make_dirs(APIGEE_CLI_DIRECTORY)
        try:
            with open(APIGEE_CLI_ACCESS_TOKEN_FILE, 'r') as f:
                access_token = f.read().strip()
        except (IOError, OSError) as e:
            pass
        finally:
            if access_token:
                decoded = jwt.decode(access_token, verify=False)
                if (
                    decoded['exp'] < int(time.time())
                    or decoded['email'].lower() != auth_obj.username.lower()
                ):
                    access_token = ""
        if not access_token:
            access_token = get_access_token(auth_obj)
            with open(APIGEE_CLI_ACCESS_TOKEN_FILE, 'w') as f:
                f.write(access_token)
        headers['Authorization'] = f'Bearer {access_token}'
    else:
        headers['Authorization'] = (
            'Basic '
            + base64.b64encode((f'{auth_obj.username}:{auth_obj.password}').encode()).decode()
        )
    return headers


def auth_with_prefix(auth_obj, org, name, file=None, key='name'):
    if file:
        with open(file) as f:
            attr = json.loads(f.read())[key]
        return with_prefix(auth_obj, org, attr)
    return with_prefix(auth_obj, org, name)


@click.command(
    help='Custom authorization commands. More information on the use cases for these commands are yet to be documented.',
    cls=AliasedGroup,
)
def auth():
    pass


@auth.command(name='get-access-token', help='request a fresh access token')
@common_auth_options
@common_verbose_options
@common_silent_options
def get_access_token_command(
    username, password, mfa_secret, token, zonename, org, profile, **kwargs
):
    console.echo(get_access_token(gen_auth(username, password, mfa_secret, token, zonename)))


@auth.command(
    help='check if user (developer) is authorized to access resource with prefix in file'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option(
    '-f',
    '--file',
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    required=True,
)
@click.option('-k', '--key', help='name of the attribute/key to check', default='name')
def file(username, password, mfa_secret, token, zonename, org, profile, file, key, **kwargs):
    console.echo(
        auth_with_prefix(
            gen_auth(username, password, mfa_secret, token, zonename),
            org,
            None,
            file=file,
            key=key,
        )
    )


@auth.command(
    help='check if user (developer) is authorized to access resource with prefix in name'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name of the resource to check', required=True)
def name(username, password, mfa_secret, token, zonename, org, profile, name, **kwargs):
    console.echo(
        auth_with_prefix(
            gen_auth(username, password, mfa_secret, token, zonename),
            org,
            name,
            file=None,
            key='name',
        )
    )
