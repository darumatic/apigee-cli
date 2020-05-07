#!/usr/bin/env python
# __main__.py

import codecs
import configparser
import os
import re
import requests
import sys
import time
from functools import update_wrapper

import click
# from click_aliases import ClickAliasedGroup

from apigee import APP
from apigee import CMD
from apigee import __version__ as version
from apigee.apiproducts.commands import apiproducts
from apigee.apis.commands import apis
from apigee.apps.commands import apps
from apigee.auth import auth
from apigee.caches.commands import caches
from apigee.cls import AliasedGroup
from apigee.configure.commands import configure
from apigee.deployments.commands import deployments
from apigee.developers.commands import developers
from apigee.exception import exception_handler
from apigee.keyvaluemaps.commands import keyvaluemaps
from apigee.maskconfigs.commands import maskconfigs
from apigee.permissions.commands import permissions
from apigee.targetservers.commands import targetservers
from apigee.userroles.commands import userroles
from apigee.utils import show_message

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"]
)


@click.group(context_settings=CONTEXT_SETTINGS, cls=AliasedGroup, invoke_without_command=False, chain=False)
# @click.group(context_settings=CONTEXT_SETTINGS, cls=ClickAliasedGroup, invoke_without_command=False, chain=False)
@click.version_option(version, '-V', '--version')
@click.pass_context
def cli(ctx):
    """Welcome to the Apigee Management API command-line interface!

    \b
    Docs:    https://mdelotavo.github.io/apigee-cli/
    PyPI:    https://pypi.org/project/apigeecli/
    GitHub:  https://github.com/mdelotavo/apigee-cli

    \f

    :param click.core.Context ctx: Click context.
    """
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

@exception_handler
def main():
    cli.add_command(configure)
    cli.add_command(deployments)
    cli.add_command(caches)
    cli.add_command(keyvaluemaps)
    cli.add_command(targetservers)
    cli.add_command(apis)
    cli.add_command(apiproducts)
    cli.add_command(apps)
    cli.add_command(developers)
    cli.add_command(auth)
    cli.add_command(maskconfigs)
    cli.add_command(userroles)
    cli.add_command(permissions)
    cli(prog_name=CMD, obj={})


if __name__ == '__main__':
    # cli() # pragma: no cover
    main() # pragma: no cover
