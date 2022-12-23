import click
from click_option_group import MutuallyExclusiveOptionGroup, optgroup

from apigee import console
from apigee.apps.apps import Apps
from apigee.auth import common_auth_options, gen_auth

# from apigee.cls import OptionEatAll
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options


@click.group(help="Management APIs available for working with developer apps.")
def apps():
    pass


def _create_developer_app(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    developer,
    body,
    **kwargs
):
    return (
        Apps(gen_auth(username, password, mfa_secret, token, zonename), org, None)
        .create_developer_app(developer, body)
        .text
    )


@apps.command(
    help="Creates an app associated with a developer, associates the app with an API product, and auto-generates an API key for the app to use in calls to API proxies inside the API product."
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="name", required=True)
@click.option("--developer", help="developer email or id", required=True)
@click.option("-b", "--body", help="request body", required=True)
def create(*args, **kwargs):
    console.echo(_create_developer_app(*args, **kwargs))


def _delete_developer_app(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    developer,
    **kwargs
):
    return (
        Apps(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .delete_developer_app(developer)
        .text
    )


@apps.command(help="Deletes a developer app.")
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="name", required=True)
@click.option("--developer", help="developer email or id", required=True)
def delete(*args, **kwargs):
    console.echo(_delete_developer_app(*args, **kwargs))


def _create_empty_developer_app(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    developer,
    display_name="",
    callback_url="",
    **kwargs
):
    return (
        Apps(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .create_empty_developer_app(
            developer, display_name=display_name, callback_url=callback_url
        )
        .text
    )


@apps.command(help="Creates an empty developer app.")
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="name", required=True)
@click.option("--developer", help="developer email or id", required=True)
@click.option(
    "--display-name",
    default=None,
    help="The DisplayName (set with an attribute) is what appears in the management UI. If you don't provide a DisplayName, the name is used.",
)
@click.option(
    "--callback-url",
    default=None,
    help="The callbackUrl is used by OAuth 2.0 authorization servers to communicate authorization codes back to apps. CallbackUrl must match the value of redirect_uri in some OAuth 2.0 See the documentation on OAuth 2.0 for more details.",
)
def create_empty(*args, **kwargs):
    console.echo(_create_empty_developer_app(*args, **kwargs))


def _get_developer_app_details(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    developer,
    **kwargs
):
    return (
        Apps(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_developer_app_details(developer)
        .text
    )


@apps.command(
    help="Get the profile of a specific developer app. All times in the response are UNIX times. Note that the response contains a top-level attribute named accessType that is no longer used by Apigee."
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="name", required=True)
@click.option("--developer", help="developer email or id", required=True)
def get(*args, **kwargs):
    console.echo(_get_developer_app_details(*args, **kwargs))


def _list_org_apps(
    username, password, mfa_secret, token, zonename, org, profile, **kwargs
):
    return (
        Apps(gen_auth(username, password, mfa_secret, token, zonename), org, None)
        .list_org_apps()
        .text
    )


@apps.command(help="Lists apps in an organisation.")
@common_auth_options
@common_verbose_options
@common_silent_options
def list_org_apps(*args, **kwargs):
    console.echo(_list_org_apps(*args, **kwargs))


def _get_org_app(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Apps(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_org_app()
        .text
    )


@apps.command(help="Gets an app in an organisation.")
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="name", required=True)
def get_org_app(*args, **kwargs):
    console.echo(_get_org_app(*args, **kwargs))


def _list_developer_apps(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    developer,
    prefix=None,
    expand=False,
    count=1000,
    startkey="",
    **kwargs
):
    return Apps(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).list_developer_apps(
        developer, prefix=prefix, expand=expand, count=count, startkey=startkey
    )


@apps.command(
    help="Lists all apps created by a developer in an organization, and optionally provides an expanded view of the apps. All time values in the response are UNIX times. You can specify either the developer's email address or Edge ID."
)
@common_auth_options
@common_verbose_options
@common_silent_options
@common_prefix_options
@click.option("--developer", help="developer email or id", required=True)
@click.option(
    "--expand/--no-expand",
    default=False,
    help="Set to true to expand the results. This query parameter does not work if you use the count or startKey query parameters.",
)
@click.option(
    "--count",
    type=click.INT,
    default=1000,
    show_default=True,
    help="Limits the list to the number you specify. The limit is 100. Use with the startKey parameter to provide more targeted filtering.",
)
@click.option(
    "--startkey",
    default="",
    show_default=True,
    help="To filter the keys that are returned, enter the name of a developer app that the list will start with.",
)
def list(*args, **kwargs):
    console.echo(_list_developer_apps(*args, **kwargs))


# def _list_apps_for_all_developers(
#     username, password, mfa_secret, token, zonename, org, profile,
#     prefix=None,
#     expand=False,
#     count=1000,
#     startkey="",
#     format="dict",
#     progress_bar=False,
# ):
#     pass


def _delete_key_for_a_developer_app(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    developer,
    consumer_key=None,
    **kwargs
):
    return (
        Apps(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .delete_key_for_a_developer_app(developer, consumer_key=consumer_key,)
        .text
    )


@apps.command(help="Deletes a custom consumer key from a developer app.")
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="app name", required=True)
@click.option("--developer", help="developer email or id", required=True)
@click.option("--consumer-key", help="consumer key", required=True)
def delete_creds(*args, **kwargs):
    console.echo(_delete_key_for_a_developer_app(*args, **kwargs))


def _update_key_for_a_developer_app(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    developer,
    consumer_key=None,
    action="",
    **kwargs
):
    return (
        Apps(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .update_key_for_a_developer_app(
            developer, consumer_key=consumer_key, action=action,
        )
        .text
    )


@apps.command(help="Approve a custom consumer key in a developer app.")
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="app name", required=True)
@click.option("--developer", help="developer email or id", required=True)
@click.option("--consumer-key", help="consumer key", required=True)
@click.option("--action", default="approve", hidden=True)
def approve_creds(*args, **kwargs):
    console.echo(_update_key_for_a_developer_app(*args, **kwargs))


@apps.command(help="Revoke a custom consumer key in a developer app.")
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="app name", required=True)
@click.option("--developer", help="developer email or id", required=True)
@click.option("--consumer-key", help="consumer key", required=True)
@click.option("--action", default="revoke", hidden=True)
def revoke_creds(*args, **kwargs):
    console.echo(_update_key_for_a_developer_app(*args, **kwargs))


def _create_a_consumer_key_and_secret(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    developer,
    consumer_key=None,
    consumer_secret=None,
    key_length=32,
    secret_length=32,
    key_suffix=None,
    key_delimiter="-",
    products=[],
    **kwargs
):
    return (
        Apps(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .create_a_consumer_key_and_secret(
            developer,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            key_length=key_length,
            secret_length=secret_length,
            key_suffix=key_suffix,
            key_delimiter=key_delimiter,
            products=products,
        )
        .text
    )


@apps.command(
    help="Creates a custom consumer key and secret for a developer app. This is particularly useful if you want to migrate existing consumer keys/secrets to Edge from another system. Consumer keys and secrets can contain letters, numbers, underscores, and hyphens. No other special characters are allowed."
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option("-n", "--name", help="app name", required=True)
@click.option("--developer", help="developer email or id", required=True)
@optgroup.group(
    "consumerKey options",
    cls=MutuallyExclusiveOptionGroup,
    help="The consumerKey options",
)
@optgroup.option("--consumer-key", default=None, help="")
@optgroup.option(
    "--key-length",
    type=click.INT,
    default=32,
    show_default=True,
    help="length of the consumer key",
)
@optgroup.group(
    "consumerSecret options",
    cls=MutuallyExclusiveOptionGroup,
    help="The consumerSecret options",
)
@optgroup.option("--consumer-secret", default=None, help="")
@optgroup.option(
    "--secret-length",
    type=click.INT,
    default=32,
    show_default=True,
    help="length of the consumer secret",
)
@click.option("--key-suffix", default=None, help="")
@click.option(
    "--key-delimiter",
    default="-",
    help="separates consumerKey and key suffix with a delimiter.",
)
@click.option(
    "--products",
    multiple=True,
    default=[],
    show_default=True,
    help="API products to be associated with the app's credentials",
)
# @click.option(
#     'products',
#     '--products',
#     metavar='LIST',
#     cls=OptionEatAll,
#     default=[],
#     help="A list of API products to be associated with the app's credentials",
# )
def create_creds(*args, **kwargs):
    # click.echo(kwargs.get('products'))
    # import sys;sys.exit(1)
    console.echo(_create_a_consumer_key_and_secret(*args, **kwargs))


# def _add_api_product_to_key(username, password, mfa_secret, token, zonename, org, profile, developer, consumer_key, request_body):
#     pass


def _restore_app(
    username, password, mfa_secret, token, zonename, org, profile, file, **kwargs
):
    return (
        Apps(gen_auth(username, password, mfa_secret, token, zonename), org, None)
        .restore_app(file)
        .text
    )


@apps.command(help="Restore developer app from a file.")
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    required=True,
)
def restore(*args, **kwargs):
    _restore_app(*args, **kwargs)
