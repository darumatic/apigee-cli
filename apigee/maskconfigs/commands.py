import click

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.maskconfigs.maskconfigs import Maskconfigs
# from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options


@click.group(help='Specify data that will be filtered out of trace sessions.')
def maskconfigs():
    pass


def _create_data_masks_for_an_api_proxy(
    username, password, mfa_secret, token, zonename, org, profile, name, body, **kwargs
):
    return (
        Maskconfigs(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .create_data_masks_for_an_api_proxy(body)
        .text
    )


@maskconfigs.command(
    help="Create a data mask for an API proxy. You can capture message content to assist in runtime debugging of APIs calls. In many cases, API traffic contains sensitive data, such credit cards or personally identifiable health information (PHI) that needs to filtered out of the captured message content. Data masks enable you to specify data that will be filtered out of trace sessions. Data masking is only enabled when a trace session (also called a 'debug' session) is enabled for an API proxy. If no trace session are enabled on an API proxy, then the data will not be masked."
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='API proxy name', required=True)
@click.option('-b', '--body', help='request body', required=True)
def create_api(*args, **kwargs):
    console.echo(_create_data_masks_for_an_api_proxy(*args, **kwargs))


def _delete_data_masks_for_an_api_proxy(
    username, password, mfa_secret, token, zonename, org, profile, name, maskconfig_name, **kwargs
):
    return (
        Maskconfigs(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .delete_data_masks_for_an_api_proxy(maskconfig_name)
        .text
    )


@maskconfigs.command(help='Delete a data mask for an API proxy.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='API proxy name', required=True)
@click.option('--maskconfig-name', help='data mask name', required=True)
def delete_api(*args, **kwargs):
    console.echo(_delete_data_masks_for_an_api_proxy(*args, **kwargs))


def _get_data_mask_details_for_an_api_proxy(
    username, password, mfa_secret, token, zonename, org, profile, name, maskconfig_name, **kwargs
):
    return (
        Maskconfigs(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_data_mask_details_for_an_api_proxy(maskconfig_name)
        .text
    )


@maskconfigs.command(help='Get the details for a data mask for an API proxy.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='API proxy name', required=True)
@click.option('--maskconfig-name', help='data mask name', required=True)
def get_api(*args, **kwargs):
    console.echo(_get_data_mask_details_for_an_api_proxy(*args, **kwargs))


def _list_data_masks_for_an_api_proxy(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Maskconfigs(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .list_data_masks_for_an_api_proxy()
        .text
    )


@maskconfigs.command(help='List all data masks for an API proxy.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='API proxy name', required=True)
def list_api(*args, **kwargs):
    console.echo(_list_data_masks_for_an_api_proxy(*args, **kwargs))


def _list_data_masks_for_an_organization(
    username, password, mfa_secret, token, zonename, org, profile, **kwargs
):
    return (
        Maskconfigs(gen_auth(username, password, mfa_secret, token, zonename), org, None)
        .list_data_masks_for_an_organization()
        .text
    )


@maskconfigs.command(help='List all data masks for an organization.')
@common_auth_options
@common_verbose_options
@common_silent_options
def list(*args, **kwargs):
    console.echo(_list_data_masks_for_an_organization(*args, **kwargs))


def _push_data_masks_for_an_api_proxy(
    username, password, mfa_secret, token, zonename, org, profile, name, file, **kwargs
):
    return Maskconfigs(
        gen_auth(username, password, mfa_secret, token, zonename), org, name
    ).push_data_masks_for_an_api_proxy(file)


@maskconfigs.command(
    help='Push data mask for an API proxy to Apigee. This will create/update a data mask.'
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='API proxy name', required=True)
@click.option(
    '-f',
    '--file',
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    required=True,
)
def push(*args, **kwargs):
    _push_data_masks_for_an_api_proxy(*args, **kwargs)
