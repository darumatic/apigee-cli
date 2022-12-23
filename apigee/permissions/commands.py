import click
from click_aliases import ClickAliasedGroup

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.permissions.permissions import Permissions
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options

TABLEFMT_CHOICES = [
    "plain",
    "simple",
    "github",
    "grid",
    "fancy_grid",
    "pipe",
    "orgtbl",
    "jira",
    "presto",
    "psql",
    "rst",
    "mediawiki",
    "moinmoin",
    "youtrack",
    "html",
    "latex",
    "latex_raw",
    "latex_booktabs",
    "textile",
]


@click.group(
    help="Permissions for roles in an organization on Apigee Edge.",
    cls=ClickAliasedGroup,
)
def permissions():
    pass


def _create_permissions(
    username, password, mfa_secret, token, zonename, org, profile, name, body, **kwargs
):
    return (
        Permissions(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .create_permissions(body)
        .text
    )


@permissions.command(help="Create permissions for a role.")
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-b", "--body", help="request body", required=True)
def create(*args, **kwargs):
    console.echo(_create_permissions(*args, **kwargs))


def _team_permissions(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    file,
    placeholder_key=None,
    placeholder_value="",
    **kwargs
):
    return (
        Permissions(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .team_permissions(
            file, placeholder_key=placeholder_key, placeholder_value=placeholder_value
        )
        .text
    )


@permissions.command(
    help="Create permissions for a role using a template file.",
    aliases=["template-permissions"],
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="the role name", required=True)
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    required=True,
)
@click.option(
    "--placeholder-key",
    default=None,
    help="placeholder key to replace with a placeholder value",
)
@click.option(
    "--placeholder-value",
    default="",
    show_default=True,
    help="placeholder value to replace placeholder key.",
)
def template(*args, **kwargs):
    console.echo(_team_permissions(*args, **kwargs))


def _get_permissions(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    format,
    showindex=False,
    tablefmt="plain",
    **kwargs
):
    return Permissions(
        gen_auth(username, password, mfa_secret, token, zonename), org, name
    ).get_permissions(
        formatted=True,
        format="text" if format == "json" else format,
        showindex=showindex,
        tablefmt=tablefmt,
    )


@permissions.command(help="Get permissions for a role.")
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name", required=True)
# @click.option("-j", "--json", help="display json output when using -r flag", default="table")
@click.option(
    "--format",
    help="defines how to format output",
    default="table",
    type=click.Choice(["json", "table"], case_sensitive=False),
)
@click.option("--showindex/--no-showindex", default=False)
@click.option(
    "--tablefmt",
    help="defines how the table is formatted",
    type=click.Choice(TABLEFMT_CHOICES, case_sensitive=False),
    default="plain",
    show_default=True,
)
def get(*args, **kwargs):
    console.echo(_get_permissions(*args, **kwargs))
