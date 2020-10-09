import click
from click_aliases import ClickAliasedGroup

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.deployments.deployments import Deployments
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options

TABLEFMT_CHOICES = [
    'plain',
    'simple',
    'github',
    'grid',
    'fancy_grid',
    'pipe',
    'orgtbl',
    'jira',
    'presto',
    'psql',
    'rst',
    'mediawiki',
    'moinmoin',
    'youtrack',
    'html',
    'latex',
    'latex_raw',
    'latex_booktabs',
    'textile',
]


@click.group(
    help='API proxies that are actively deployed in environments on Apigee Edge.',
    cls=ClickAliasedGroup,
)
def deployments():
    pass


def _get_api_proxy_deployment_details(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    format,
    showindex,
    tablefmt,
    revision_name_only,
    **kwargs
):
    return Deployments(
        gen_auth(username, password, mfa_secret, token, zonename), org, name
    ).get_api_proxy_deployment_details(
        formatted=True,
        format=format,
        showindex=showindex,
        tablefmt=tablefmt,
        revision_name_only=revision_name_only,
    )


@deployments.command(
    help='Returns detail on all deployments of the API proxy for all environments. All deployments are listed in the test and prod environments, as well as other environments, if they exist.',
    aliases=['get-api-proxy-deployment-details'],
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
# @click.option("-j", "--json", help="display json output when using -r flag", default="table")
@click.option(
    '--format',
    help='defines how to format output when using the -r flag',
    default='table',
    type=click.Choice(['json', 'table'], case_sensitive=False),
)
@click.option('--showindex/--no-showindex', default=False)
@click.option(
    '--tablefmt',
    help='defines how the table is formatted',
    type=click.Choice(TABLEFMT_CHOICES, case_sensitive=False),
    default='plain',
    show_default=True,
)
@click.option('--revision-name-only/--no-revision-name-only', '-r/-R', default=False)
def get(*args, **kwargs):
    console.echo(_get_api_proxy_deployment_details(*args, **kwargs))
