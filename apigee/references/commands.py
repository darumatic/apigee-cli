import click

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.prefix import common_prefix_options
from apigee.references.references import References
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options


@click.group(help="References in an organization and environment.")
def references():
    pass


def _list_all_references(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    environment,
    prefix=None,
    **kwargs
):
    return References(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).list_all_references(environment, prefix=prefix)


@references.command(help="List all references in an organization and environment.")
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option("-e", "--environment", help="environment", required=True)
def list(*args, **kwargs):
    console.echo(_list_all_references(*args, **kwargs))


def _get_reference(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    **kwargs
):
    return (
        References(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_reference(environment)
        .text
    )


@references.command(help="Get reference in an organization and environment.")
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="reference name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
def get(*args, **kwargs):
    console.echo(_get_reference(*args, **kwargs))


def _delete_reference(*args, **kwargs):
    pass


@references.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def delete(*args, **kwargs):
    _delete_reference(*args, **kwargs)


def _create_reference(*args, **kwargs):
    pass


@references.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def create(*args, **kwargs):
    _create_reference(*args, **kwargs)


def _update_reference(*args, **kwargs):
    pass


@references.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def update(*args, **kwargs):
    _update_reference(*args, **kwargs)
