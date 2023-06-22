import click

from apigee.auth import common_auth_options, generate_authentication
from apigee.backups.backups import BackupConfig, Backups
from apigee.exceptions import InvalidApisError
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.types import APIGEE_API_CHOICES
from apigee.verbose import common_verbose_options


@click.group(
    help="Download configuration files from Apigee that can later be restored."
)
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
    for choice in apis:
        if choice not in APIGEE_API_CHOICES:
            raise InvalidApisError(f"The choice '{choice}' is not a valid APIGEE API choice.")
    if not isinstance(apis, set):
        apis = set(apis)
    config = BackupConfig(
        authentication=generate_authentication(username, password, mfa_secret, token, zonename),
        org_name=org,
        working_directory=target_directory,
        prefix=prefix,
        api_choices=apis,
        environments=list(environments)
    )
    Backups(config).generate_snapshot_files_and_download_data()


@backups.command(
    help="Downloads and generates local snapshots of specified Apigee resources e.g. API proxies, KVMs, target servers, etc."
)
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option(
    "--target-directory",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=False),
    required=True,
)
@click.option(
    "--apis",
    type=click.Choice(APIGEE_API_CHOICES, case_sensitive=False),
    multiple=True,
    default=APIGEE_API_CHOICES,
    show_default=True,
)
# @click.option('--apis', metavar='LIST', cls=OptionEatAll, default=APIS_CHOICES, show_default=True, help='')
# @click.option(
#     '-e', '--environments', metavar='LIST', cls=OptionEatAll, default=['test', 'prod'], help=''
# )
@click.option(
    "-e",
    "--environments",
    multiple=True,
    show_default=True,
    default=["test", "prod"],
    help="",
)
def take_snapshot(*args, **kwargs):
    _take_snapshot(*args, **kwargs)
