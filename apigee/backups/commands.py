import click

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.backups.backups import Backups
from apigee.cls import OptionEatAll
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options

APIS_CHOICES = {
    'apis',
    'keyvaluemaps',
    'targetservers',
    'caches',
    'developers',
    'apiproducts',
    'apps',
    'userroles',
}


@click.group(help='Download configuration files from Apigee that can later be restored.')
def backups():
    pass


def _take_snapshot(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    target_directory,
    prefix,
    environments,
    apis,
    **kwargs
):
    if not isinstance(apis, set):
        apis = set(apis)
    return Backups(
        gen_auth(username, password, mfa_secret, token, zonename),
        org,
        target_directory,
        prefix=prefix,
        fs_write=True,
        apis=apis,
        environments=environments,
    ).take_snapshot()


@backups.command(
    help='Downloads and generates local snapshots of specified Apigee resources e.g. API proxies, KVMs, target servers, etc.'
)
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option(
    '--target-directory',
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=False),
    required=True,
)
@click.option(
    '--apis',
    type=click.Choice(APIS_CHOICES, case_sensitive=False),
    multiple=True,
    default=APIS_CHOICES,
    show_default=True,
)
# @click.option('--apis', metavar='LIST', cls=OptionEatAll, default=APIS_CHOICES, show_default=True, help='')
@click.option(
    '-e', '--environments', metavar='LIST', cls=OptionEatAll, default=['test', 'prod'], help=''
)
def take_snapshot(*args, **kwargs):
    _take_snapshot(*args, **kwargs)
