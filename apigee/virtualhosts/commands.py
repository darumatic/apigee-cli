import click

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options
from apigee.virtualhosts.virtualhosts import Virtualhosts


@click.group(
    help="A named network configuration (including URL) for an environment (for example 'test' or 'prod') on API Services."
)
def virtualhosts():
    pass


def _create_a_virtual_host_for_an_environment(*args, **kwargs):
    pass


@virtualhosts.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def create(*args, **kwargs):
    _create_a_virtual_host_for_an_environment(*args, **kwargs)


def _delete_a_virtual_host_from_an_environment(*args, **kwargs):
    pass


@virtualhosts.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def delete(*args, **kwargs):
    _delete_a_virtual_host_from_an_environment(*args, **kwargs)


def _get_a_virtual_host_for_an_environment(
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
        Virtualhosts(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .get_a_virtual_host_for_an_environment(environment)
        .text
    )


@virtualhosts.command(help="Gets details for a named virtual host.")
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="reference name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
def get(*args, **kwargs):
    console.echo(_get_a_virtual_host_for_an_environment(*args, **kwargs))


def _list_virtual_hosts_for_an_environment(
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
    return Virtualhosts(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).list_virtual_hosts_for_an_environment(environment, prefix=prefix)


@virtualhosts.command(help="Get a list of named virtual hosts for an environment.")
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option("-e", "--environment", help="environment", required=True)
def list(*args, **kwargs):
    console.echo(_list_virtual_hosts_for_an_environment(*args, **kwargs))


def _update_virtual_host_for_an_environment(*args, **kwargs):
    pass


@virtualhosts.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def update(*args, **kwargs):
    _update_virtual_host_for_an_environment(*args, **kwargs)
