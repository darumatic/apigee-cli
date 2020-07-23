import click

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.targetservers.targetservers import Targetservers
from apigee.verbose import common_verbose_options


@click.group(
    help='TargetServers are used to decouple TargetEndpoint HTTPTargetConnections from concrete URLs for backend services.'
)
def targetservers():
    pass


def _create_a_targetserver(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    body,
    **kwargs
):
    return (
        Targetservers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .create_a_targetserver(environment, body)
        .text
    )


@targetservers.command(
    help='Create a TargetServer in the specified environment. TargetServers are used to decouple TargetEndpoint HTTPTargetConnections from concrete URLs for backend services.'
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-b', '--body', help='request body', required=True)
def create(*args, **kwargs):
    console.echo(_create_a_targetserver(*args, **kwargs))


def _delete_a_targetserver(
    username, password, mfa_secret, token, zonename, org, profile, name, environment, **kwargs
):
    return (
        Targetservers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .delete_a_targetserver(environment)
        .text
    )


@targetservers.command(
    help='Delete a TargetServer configuration from an environment. Returns information about the deleted TargetServer.'
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
def delete(*args, **kwargs):
    console.echo(_delete_a_targetserver(*args, **kwargs))


def _list_targetservers_in_an_environment(
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
    return Targetservers(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).list_targetservers_in_an_environment(environment, prefix=prefix)


@targetservers.command(help='List all TargetServers in an environment.')
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option('-e', '--environment', help='environment', required=True)
def list(*args, **kwargs):
    console.echo(_list_targetservers_in_an_environment(*args, **kwargs))


def _get_targetserver(
    username, password, mfa_secret, token, zonename, org, profile, name, environment, **kwargs
):
    return (
        Targetservers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_targetserver(environment)
        .text
    )


@targetservers.command(help='Returns a TargetServer definition.')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
def get(*args, **kwargs):
    console.echo(_get_targetserver(*args, **kwargs))


def _update_a_targetserver(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    body,
    **kwargs
):
    return (
        Targetservers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .update_a_targetserver(environment, body)
        .text
    )


@targetservers.command(help='Modifies an existing TargetServer.')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-b', '--body', help='request body', required=True)
def create(*args, **kwargs):
    console.echo(_update_a_targetserver(*args, **kwargs))


def _push_targetserver(
    username, password, mfa_secret, token, zonename, org, profile, environment, file, **kwargs
):
    return Targetservers(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).push_targetserver(environment, file)


@targetservers.command(
    help='Push TargetServer to Apigee. This will create/update a TargetServer.'
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-e', '--environment', help='environment', required=True)
@click.option(
    '-f',
    '--file',
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    required=True,
)
def push(*args, **kwargs):
    _push_targetserver(*args, **kwargs)
