import click

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.developers.developers import Developers
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options


@click.group(
    help='Developers implement client/consumer apps and must be registered with an organization on Apigee Edge.'
)
def developers():
    pass


def _create_developer(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    first_name,
    last_name,
    user_name,
    attributes='{"attributes" : [ ]}',
    **kwargs
):
    return (
        Developers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .create_developer(first_name, last_name, user_name, attributes=attributes)
        .text
    )


@developers.command(
    help='Creates a profile for a developer in an organization. Once created, the developer can register an app and receive an API key.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option(
    '-n',
    '--name',
    help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
    required=True,
)
@click.option('--first-name', help='The first name of the developer.', required=True)
@click.option('--last-name', help='The last name of the developer.', required=True)
@click.option(
    '--user-name',
    help="The developer's username. This value is not used by Apigee Edge.",
    required=True,
)
@click.option(
    '--attributes',
    default='{"attributes" : [ ]}',
    required=True,
    help='request body e.g.: \'{"attributes" : [ ]}\'',
)
def create(*args, **kwargs):
    console.echo(_create_developer(*args, **kwargs))


def _delete_developer(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Developers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .delete_developer()
        .text
    )


@developers.command(
    help='Deletes a developer from an organization. All apps and API keys associated with the developer are also removed from the organization. All times in the response are UNIX times. To avoid permanently deleting developers and their artifacts, consider deactivating developers instead.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option(
    '-n',
    '--name',
    help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
    required=True,
)
def delete(*args, **kwargs):
    console.echo(_delete_developer(*args, **kwargs))


def _get_developer(username, password, mfa_secret, token, zonename, org, profile, name, **kwargs):
    return (
        Developers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_developer()
        .text
    )


@developers.command(
    help="Returns the profile for a developer by email address or ID. All time values are UNIX time values. The profile includes the developer's email address, ID, name, and other information."
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option(
    '-n',
    '--name',
    help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
    required=True,
)
def get(*args, **kwargs):
    console.echo(_get_developer(*args, **kwargs))


def _get_developer_by_app(
    username, password, mfa_secret, token, zonename, org, profile, app_name, **kwargs
):
    return (
        Developers(gen_auth(username, password, mfa_secret, token, zonename), org, None)
        .get_developer_by_app(app_name)
        .text
    )


@developers.command(
    help='Gets the developer profile by app name. The profile retrieved is for the developer associated with the app in the organization. All time values are UNIX time values.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('--app-name', help='the app name', required=True)
def get_by_app(*args, **kwargs):
    console.echo(_get_developer_by_app(*args, **kwargs))


def _list_developers(
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
    return Developers(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).list_developers(prefix=prefix, expand=expand, count=count, startkey=startkey)


@developers.command(
    help='Lists all developers in an organization by email address. This call does not list any company developers who are a part of the designated organization.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@common_prefix_options
@click.option(
    '--expand/--no-expand',
    default=False,
    help='Set to true to list developers exanded with details.',
)
@click.option(
    '--count',
    type=click.INT,
    default=1000,
    show_default=True,
    help='Limits the list to the number you specify. Use with the startKey parameter to provide more targeted filtering. The limit is 1000.',
)
@click.option(
    '--startkey',
    default="",
    show_default=True,
    help='To filter the keys that are returned, enter the email of a developer that the list will start with.',
)
def list(*args, **kwargs):
    console.echo(_list_developers(*args, **kwargs))


def _set_developer_status(
    username, password, mfa_secret, token, zonename, org, profile, name, action, **kwargs
):
    return (
        Developers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .set_developer_status(action)
        .text
    )


@developers.command(
    help="Sets a developer's status to active or inactive for a specific organization. Run this API for each organization where you want to change the developer's status."
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option(
    '-n',
    '--name',
    help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
    required=True,
)
@click.option(
    '--action',
    type=click.Choice(['active', 'inactive'], case_sensitive=False),
    required=True,
    show_default=True,
)
def set_status(*args, **kwargs):
    console.echo(_set_developer_status(*args, **kwargs))


def _update_developer(
    username, password, mfa_secret, token, zonename, org, profile, name, body, **kwargs
):
    return (
        Developers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .update_developer(body)
        .text
    )


@developers.command(
    help='Update an existing developer profile. To add new values or update existing values, submit the new or updated portion of the developer profile along with the rest of the developer profile, even if no values are changing. To delete attributes from a developer profile, submit the entire profile without the attributes that you want to delete.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option(
    '-n',
    '--name',
    help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
    required=True,
)
@click.option('-b', '--body', help='request body', required=True)
def update(*args, **kwargs):
    console.echo(_update_developer(*args, **kwargs))


# def _get_developer_attribute(username, password, mfa_secret, token, zonename, org, profile, attribute_name, **kwargs):
#     pass


def _update_a_developer_attribute(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    attribute_name,
    updated_value,
    **kwargs
):
    return (
        Developers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .update_a_developer_attribute(attribute_name, updated_value)
        .text
    )


@developers.command(help='Updates the value of a developer attribute.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option(
    '-n',
    '--name',
    help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
    required=True,
)
@click.option('--attribute-name', help='attribute name', required=True)
@click.option('--updated-value', help='updated value', required=True)
def update_attr(*args, **kwargs):
    console.echo(_update_a_developer_attribute(*args, **kwargs))


def _delete_developer_attribute(
    username, password, mfa_secret, token, zonename, org, profile, name, attribute_name, **kwargs
):
    return (
        Developers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .delete_developer_attribute(attribute_name)
        .text
    )


@developers.command(help='Deletes a developer attribute.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option(
    '-n',
    '--name',
    help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
    required=True,
)
@click.option('--attribute-name', help='attribute name', required=True)
def delete_attr(*args, **kwargs):
    console.echo(_delete_developer_attribute(*args, **kwargs))


def _get_all_developer_attributes(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Developers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_all_developer_attributes()
        .text
    )


@developers.command(help='Returns a list of all developer attributes.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option(
    '-n',
    '--name',
    help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
    required=True,
)
def get_attrs(*args, **kwargs):
    console.echo(_get_all_developer_attributes(*args, **kwargs))


def _update_all_developer_attributes(
    username, password, mfa_secret, token, zonename, org, profile, name, body, **kwargs
):
    return (
        Developers(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .update_all_developer_attributes(body)
        .text
    )


@developers.command(
    help='Updates or creates developer attributes. This API replaces the current list of attributes with the attributes specified in the request body. This lets you update existing attributes, add new attributes, or delete existing attributes by omitting them from the request body.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option(
    '-n',
    '--name',
    help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
    required=True,
)
@click.option('-b', '--body', help='request body', required=True)
def update_all_attrs(*args, **kwargs):
    console.echo(_update_all_developer_attributes(*args, **kwargs))
