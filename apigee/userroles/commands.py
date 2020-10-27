import click

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.cls import OptionEatAll
# from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.userroles.userroles import Userroles
from apigee.verbose import common_verbose_options


@click.group(
    help='Roles for users in an organization on Apigee Edge. User roles form the basis of role-based access in Apigee Edge. Users are associated with one or more userroles. Each userrole defines a set of permissions (GET, PUT, DELETE) on RBAC resources (defined by URI paths).'
)
def userroles():
    pass


def _add_a_user_to_a_role(
    username, password, mfa_secret, token, zonename, org, profile, name, user_email, **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .add_a_user_to_a_role(user_email)
        .text
    )


@userroles.command(help='Add a user to a role.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
@click.option('--user-email', help='the email address of the user', required=True)
def add_user(*args, **kwargs):
    console.echo(_add_a_user_to_a_role(*args, **kwargs))


def _add_permissions_for_a_resource_to_a_user_role(
    username, password, mfa_secret, token, zonename, org, profile, name, body, **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .add_permissions_for_a_resource_to_a_user_role(body)
        .text
    )


@userroles.command(help='Add Permissions for Resource to a Role')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
@click.option('-b', '--body', help='request body', required=True)
def add_permissions(*args, **kwargs):
    console.echo(_add_permissions_for_a_resource_to_a_user_role(*args, **kwargs))


def _add_permissions_for_multiple_resources_to_a_user_role(
    username, password, mfa_secret, token, zonename, org, profile, name, body, **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .add_permissions_for_multiple_resources_to_a_user_role(body)
        .text
    )


@userroles.command(help='Adds multiple permissions to multiple resources simultaneously.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
@click.option('-b', '--body', help='request body', required=True)
def add_permissions_multiple(*args, **kwargs):
    console.echo(_add_permissions_for_multiple_resources_to_a_user_role(*args, **kwargs))


def _create_a_user_role_in_an_organization(
    username, password, mfa_secret, token, zonename, org, profile, names, **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, names)
        .create_a_user_role_in_an_organization()
        .text
    )


@userroles.command(help='Creates one or more user roles in an organization.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option(
    '-n', '--names', metavar='LIST', cls=OptionEatAll, help='list of role names', required=True
)
def create(*args, **kwargs):
    console.echo(_create_a_user_role_in_an_organization(*args, **kwargs))


def _delete_a_permission_for_a_resource(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    permission,
    resource_path,
    **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .delete_a_permission_for_a_resource(permission, resource_path)
        .text
    )


@userroles.command(
    help='Removes a permission from a resource for the role specified. Permissions are case sensitive. Specify the permission as get, put, or delete.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
@click.option('--permission', help='get, put, or delete', required=True)
@click.option('--resource-path', help='the resource path', required=True)
def delete_permission(*args, **kwargs):
    console.echo(_delete_a_permission_for_a_resource(*args, **kwargs))


def _delete_resource_from_permissions(
    username, password, mfa_secret, token, zonename, org, profile, name, resource_path, **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .delete_resource_from_permissions(resource_path)
        .text
    )


@userroles.command(
    help='Removes all permissions for a resource for the role specified. Permissions are case sensitive.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
@click.option('--resource-path', help='the resource path', required=True)
def delete_resource(*args, **kwargs):
    console.echo(_delete_resource_from_permissions(*args, **kwargs))


def _delete_a_user_role(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .delete_a_user_role()
        .text
    )


@userroles.command(
    help='Deletes a role from an organization. Roles can only be deleted when no users are in the role.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
def delete(*args, **kwargs):
    console.echo(_delete_a_user_role(*args, **kwargs))


def _get_a_role(username, password, mfa_secret, token, zonename, org, profile, name, **kwargs):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_a_role()
        .text
    )


@userroles.command(help='Gets the name of a user role.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
def get(*args, **kwargs):
    console.echo(_get_a_role(*args, **kwargs))


def _get_resource_permissions_for_a_specific_role(
    username, password, mfa_secret, token, zonename, org, profile, name, resource_path="", **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_resource_permissions_for_a_specific_role(resource_path=resource_path)
        .text
    )


@userroles.command(help='Gets a list of permissions associated with the specified resource.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
@click.option('--resource-path', help='the resource path', required=True)
def get_permissions(*args, **kwargs):
    console.echo(_get_resource_permissions_for_a_specific_role(*args, **kwargs))


def _get_users_for_a_role(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_users_for_a_role()
        .text
    )


@userroles.command(help='Returns a list of all system users associated with a role.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
def get_users(*args, **kwargs):
    console.echo(_get_users_for_a_role(*args, **kwargs))


def _list_permissions_for_a_resource(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .list_permissions_for_a_resource()
        .text
    )


@userroles.command(help='Gets permissions for all resources associated with a user role.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
def list_permissions(*args, **kwargs):
    console.echo(_list_permissions_for_a_resource(*args, **kwargs))


def _list_user_roles(username, password, mfa_secret, token, zonename, org, profile, **kwargs):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, None)
        .list_user_roles()
        .text
    )


@userroles.command(help='Gets a list of roles available to users in an organization.')
@common_auth_options
@common_verbose_options
@common_silent_options
# @common_prefix_options
def list(*args, **kwargs):
    console.echo(_list_user_roles(*args, **kwargs))


def _remove_user_membership_in_role(
    username, password, mfa_secret, token, zonename, org, profile, name, user_email, **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .remove_user_membership_in_role(user_email)
        .text
    )


@userroles.command(help='Remove user membership in role.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
@click.option('--user-email', help='the email address of the user', required=True)
def remove_user(*args, **kwargs):
    console.echo(_remove_user_membership_in_role(*args, **kwargs))


def _verify_a_user_roles_permission_on_a_specific_RBAC_resource(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    permission,
    resource_path,
    **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .verify_a_user_roles_permission_on_a_specific_RBAC_resource(permission, resource_path)
        .text
    )


@userroles.command(
    help="Verifies that a user role's permission on a specific resource exists. Returns a value of true or false."
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
@click.option('--permission', help='get, put, or delete', required=True)
@click.option('--resource-path', help='the resource path', required=True)
def verify_permission(*args, **kwargs):
    console.echo(_verify_a_user_roles_permission_on_a_specific_RBAC_resource(*args, **kwargs))


def _verify_user_role_membership(
    username, password, mfa_secret, token, zonename, org, profile, name, user_email, **kwargs
):
    return (
        Userroles(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .verify_user_role_membership(user_email)
        .text
    )


@userroles.command(help='Verify user role membership.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='the role name', required=True)
@click.option('--user-email', help='the email address of the user', required=True)
def verify_membership(*args, **kwargs):
    console.echo(_verify_user_role_membership(*args, **kwargs))
