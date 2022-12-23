import configparser
import sys

import click
from click_aliases import ClickAliasedGroup

from apigee import APIGEE_CLI_CREDENTIALS_FILE, APIGEE_CLI_DIRECTORY
from apigee.utils import make_dirs


class HiddenSecret(object):
    def __init__(self, secret=""):
        self.secret = secret

    def __str__(self):
        return "*" * 16 if self.secret else ""


KEY_LIST = (
    "username",
    "password",
    "mfa_secret",
    "is_token",
    "zonename",
    "org",
    "prefix",
)
config = configparser.ConfigParser()
config.read(APIGEE_CLI_CREDENTIALS_FILE)
profile = "default"

for i, arg in enumerate(sys.argv):
    if arg == "-P" or arg == "--profile":
        try:
            profile = sys.argv[i + 1]
        except IndexError:
            pass
try:
    profile_dict = dict(config._sections[profile])
    for key in KEY_LIST:
        if key not in profile_dict:
            profile_dict[key] = ""
except KeyError:
    profile_dict = {k: "" for k in KEY_LIST}

# @click.group(cls=ClickAliasedGroup)
# @click.command(aliases=['conf', 'config', 'cfg'])
@click.command(help="Configure Apigee Edge credentials.")
@click.option(
    "-u",
    "--username",
    prompt="Apigee username (email)",
    default=profile_dict["username"],
    show_default=True,
)
@click.option(
    "-p",
    "--password",
    prompt="Apigee password",
    default=lambda: HiddenSecret(profile_dict["password"]),
    hide_input=True,
    show_default="hidden" if profile_dict["password"] else "None",
)
@click.option(
    "-mfa",
    "--mfa-secret",
    prompt="Apigee MFA key (optional)",
    default=lambda: HiddenSecret(profile_dict["mfa_secret"]),
    hide_input=True,
    show_default="hidden" if profile_dict["mfa_secret"] else "None",
)
@click.option(
    "-z",
    "--zonename",
    prompt="Identity zone name (to support SAML authentication)",
    default=profile_dict["zonename"],
    show_default=True,
)
@click.option(
    "--token/--no-token",
    default=True if profile_dict["is_token"] in (True, "True", "true", "1") else False,
    help="specify to use oauth without MFA",
    prompt="Use OAuth, no MFA (optional)?",
    show_default=True,
)
@click.option(
    "-o",
    "--org",
    prompt="Default Apigee organization (recommended)",
    default=profile_dict["org"],
    show_default=True,
)
@click.option(
    "--prefix",
    prompt="Default team/resource prefix (optional)",
    default=profile_dict["prefix"],
    show_default=True,
)
@click.option(
    "-P",
    "--profile",
    help="name of the user profile to create/update",
    default="default",
    show_default=True,
)
def configure(username, password, mfa_secret, token, zonename, org, prefix, profile):
    if isinstance(password, HiddenSecret):
        password = password.secret
    if isinstance(mfa_secret, HiddenSecret):
        mfa_secret = mfa_secret.secret
    profile_dict["username"] = username
    profile_dict["password"] = password
    profile_dict["mfa_secret"] = mfa_secret
    profile_dict["is_token"] = token
    profile_dict["zonename"] = zonename
    profile_dict["org"] = org
    profile_dict["prefix"] = prefix
    config[profile] = {k: v for k, v in profile_dict.items() if v}
    make_dirs(APIGEE_CLI_DIRECTORY)
    with open(APIGEE_CLI_CREDENTIALS_FILE, "w") as cf:
        config.write(cf)
