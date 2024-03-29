#!/usr/bin/env python
# __main__.py

from functools import update_wrapper

import click

from apigee import (APIGEE_CLI_EXCEPTIONS_LOG_FILE, APIGEE_CLI_PLUGINS_DIRECTORY, CMD)
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
from apigee.exceptions import wrap_with_exception_handling, configure_global_logger
from apigee.keystores.commands import keystores
from apigee.keyvaluemaps.commands import keyvaluemaps
from apigee.maskconfigs.commands import maskconfigs
from apigee.permissions.commands import permissions
from apigee.plugins.commands import plugins
from apigee.references.commands import references
from apigee.sharedflows.commands import sharedflows
from apigee.targetservers.commands import targetservers
from apigee.userroles.commands import userroles
from apigee.utils import (import_plugins_from_directory, execute_function_on_directory_files)
from apigee.virtualhosts.commands import virtualhosts

# from click_aliases import ClickAliasedGroup


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(
    context_settings=CONTEXT_SETTINGS,
    cls=AliasedGroup,
    invoke_without_command=False,
    chain=False,
)
# @click.group(context_settings=CONTEXT_SETTINGS, cls=ClickAliasedGroup, invoke_without_command=False, chain=False)
@click.version_option(version, "-V", "--version")
@click.pass_context
def cli(ctx):
    """Welcome to the (Unofficial) Apigee Management API command-line interface!

    \b
    Docs:    https://darumatic.github.io/apigee-cli/
    PyPI:    https://pypi.org/project/apigeecli/
    GitHub:  https://github.com/darumatic/apigee-cli

    \f

    :param click.core.Context ctx: Click context.
    """
    ctx.ensure_object(dict)


@wrap_with_exception_handling
def main():
    configure_global_logger(APIGEE_CLI_EXCEPTIONS_LOG_FILE)

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

    execute_function_on_directory_files(
        APIGEE_CLI_PLUGINS_DIRECTORY,
        import_plugins_from_directory,
        args=(cli_commands,),
        glob="[!.][!__]*/__init__.py",
    )

    for command in cli_commands:
        cli.add_command(command)

    cli(prog_name=CMD, obj={})


if __name__ == "__main__":
    # cli() # pragma: no cover
    main()  # pragma: no cover
