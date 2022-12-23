import click

from apigee import console
from apigee.apiproducts.apiproducts import Apiproducts
from apigee.auth import common_auth_options, gen_auth
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options


@click.group(
    help="API products enable you to bundle and distribute your APIs to multiple developer groups simultaneously, without having to modify code."
)
def apiproducts():
    pass


def _create_api_product(
    username, password, mfa_secret, token, zonename, org, profile, name, body, **kwargs
):
    return (
        Apiproducts(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .create_api_product(body)
        .text
    )


@apiproducts.command(help="Creates an API product in an organization.")
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-b", "--body", help="request body", required=True)
def create(*args, **kwargs):
    console.echo(_create_api_product(*args, **kwargs))


def _delete_api_product(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Apiproducts(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .delete_api_product()
        .text
    )


@apiproducts.command(help="Deletes an API product from an organization.")
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="name", required=True)
def delete(*args, **kwargs):
    console.echo(_delete_api_product(*args, **kwargs))


def _get_api_product(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Apiproducts(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .get_api_product()
        .text
    )


@apiproducts.command(
    help='Gets configuration data for an API product. The API product name required in the request URL is not the "Display Name" value displayed for the API product in the Edge UI. While they may be the same, they are not always the same depending on whether the API product was created via UI or API.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="name", required=True)
def get(*args, **kwargs):
    console.echo(_get_api_product(*args, **kwargs))


def _list_api_products(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    prefix=None,
    expand=False,
    count=1000,
    startkey="",
    **kwargs
):
    return Apiproducts(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).list_api_products(prefix=prefix, expand=expand, count=count, startkey=startkey)


@apiproducts.command(help="Get a list of all API product names for an organization.")
@common_auth_options
@common_verbose_options
@common_silent_options
@common_prefix_options
@click.option(
    "--expand/--no-expand",
    default=False,
    help="Set to 'true' to get expanded details about each product.",
)
@click.option(
    "--count",
    type=click.INT,
    default=1000,
    show_default=True,
    help="Number of API products to return in the API call. The maximum limit is 1000. Use with the startkey to provide more targeted filtering.",
)
@click.option(
    "--startkey",
    default="",
    show_default=True,
    help="Returns a list of API products starting with the specified API product.",
)
def list(*args, **kwargs):
    console.echo(_list_api_products(*args, **kwargs))


def _update_api_product(
    username, password, mfa_secret, token, zonename, org, profile, name, body, **kwargs
):
    return (
        Apiproducts(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .update_api_product(body)
        .text
    )


@apiproducts.command(
    help="Updates an existing API product. You must include all required values, whether or not you are updating them, as well as any optional values that you are updating."
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-b", "--body", help="request body", required=True)
def update(*args, **kwargs):
    console.echo(_update_api_product(*args, **kwargs))


def _push_apiproducts(
    username, password, mfa_secret, token, zonename, org, profile, file, **kwargs
):
    return Apiproducts(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).push_apiproducts(file)


@apiproducts.command(
    help="Push API product to Apigee. This will create/update an API product."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    required=True,
)
def push(*args, **kwargs):
    _push_apiproducts(*args, **kwargs)
