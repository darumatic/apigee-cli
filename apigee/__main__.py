#!/usr/bin/env python
# __main__.py

import codecs
import configparser
import importlib
import os
import re
import sys
import time
from functools import update_wrapper

import click
import requests

from apigee import (APIGEE_CLI_PLUGINS_DIRECTORY, APIGEE_CLI_PLUGINS_PATH, APP,
                    CMD)
from apigee import __version__ as version
from apigee.apiproducts.commands import apiproducts
from apigee.apis.commands import apis
from apigee.apps.commands import apps
from apigee.auth import auth
from apigee.backups.commands import backups
from apigee.caches.commands import caches
from apigee.cls import AliasedGroup
from apigee.configure.commands import configure
from apigee.deployments.commands import deployments
from apigee.developers.commands import developers
from apigee.exceptions import exception_handler
from apigee.keystores.commands import keystores
from apigee.keyvaluemaps.commands import keyvaluemaps
from apigee.maskconfigs.commands import maskconfigs
from apigee.permissions.commands import permissions
from apigee.plugins.commands import plugins
from apigee.references.commands import references
from apigee.sharedflows.commands import sharedflows
from apigee.targetservers.commands import targetservers
from apigee.userroles.commands import userroles
from apigee.utils import is_dir, run_func_on_dir_files, show_message
from apigee.virtualhosts.commands import virtualhosts

# from click_aliases import ClickAliasedGroup


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    context_settings=CONTEXT_SETTINGS, cls=AliasedGroup, invoke_without_command=False, chain=False
)
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
    cli_commands = {
        backups,
        configure,
        deployments,
        caches,
        keyvaluemaps,
        targetservers,
        apis,
        apiproducts,
        apps,
        developers,
        auth,
        maskconfigs,
        userroles,
        permissions,
        sharedflows,
        keystores,
        references,
        virtualhosts,
        plugins,
    }

    def _load_all_modules_in_directory(plugins_init_file):
        try:
            spec = importlib.util.spec_from_file_location('plugins_modules', plugins_init_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            import plugins_modules
            from plugins_modules import __all__ as all_plugins_modules

            for module in all_plugins_modules:
                _module = getattr(plugins_modules, module)
                if isinstance(_module, (click.core.Command, click.core.Group)):
                    cli_commands.add(_module)
        except ImportError:
            pass

    run_func_on_dir_files(
        APIGEE_CLI_PLUGINS_DIRECTORY, _load_all_modules_in_directory, glob='[!.][!__]*/__init__.py'
    )

    for command in cli_commands:
        cli.add_command(command)

    cli(prog_name=CMD, obj={})


if __name__ == '__main__':
    # cli() # pragma: no cover
    main()  # pragma: no cover
