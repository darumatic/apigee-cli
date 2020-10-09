import click
from click_option_group import MutuallyExclusiveOptionGroup, optgroup

from apigee import console
from apigee.apis.apis import Apis
from apigee.apis.deploy import deploy as deploy_tool
from apigee.auth import common_auth_options, gen_auth
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.types import Struct
from apigee.verbose import common_verbose_options


@click.group(
    help='The proxy APIs let you perform operations on API proxies, such as create, delete, update, and deploy.'
)
def apis():
    pass


def _delete_api_proxy_revision(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    revision_number,
    **kwargs,
):
    return (
        Apis(gen_auth(username, password, mfa_secret, token, zonename), org)
        .delete_api_proxy_revision(name, revision_number)
        .text
    )


@apis.command(
    help='Deletes a revision of an API proxy and all policies, resources, endpoints, and revisions associated with it. The API proxy revision must be undeployed before you can delete it.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
def delete_revision(*args, **kwargs):
    console.echo(_delete_api_proxy_revision(*args, **kwargs))


def _deploy_api_proxy_revision(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    revision_number,
    delay=0,
    override=False,
    **kwargs,
):
    return (
        Apis(gen_auth(username, password, mfa_secret, token, zonename), org)
        .deploy_api_proxy_revision(
            name, environment, revision_number, delay=delay, override=override
        )
        .text
    )


@apis.command(
    help='Deploys a revision of an existing API proxy to an environment in an organization.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
@click.option(
    '--delay',
    type=click.INT,
    default=0,
    help='Enforces a delay, measured in seconds, before the currently deployed API proxy revision is undeployed and replaced by the new revision that is being deployed. Use this setting to minimize the impact of deployment on in-flight transactions. The default value is 0.',
)
@click.option(
    '--override/--no-override',
    default=False,
    help='Flag that specifies whether to use seamless deployment to ensure zero downtime. Set this flag to "true" to instruct Edge to deploy the new revision fully before undeploying the existing revision. Use in conjunction with the delay parameter to control when the existing revision is undeployed.',
)
def deploy_revision(*args, **kwargs):
    console.echo(_deploy_api_proxy_revision(*args, **kwargs))


def _delete_undeployed_revisions(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    save_last=0,
    dry_run=False,
    **kwargs,
):
    return Apis(
        gen_auth(username, password, mfa_secret, token, zonename), org
    ).delete_undeployed_revisions(name, save_last=save_last, dry_run=dry_run)


@apis.command(
    help='Deletes all undeployed revisions of an API proxy and all policies, resources, endpoints, and revisions associated with it.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option(
    '--save-last',
    type=click.INT,
    help='denotes not to delete the N most recent revisions',
    default=0,
)
@click.option(
    '--dry-run/--no-dry-run',
    default=False,
    help='show revisions to be deleted but do not delete',
)
def clean(*args, **kwargs):
    _delete_undeployed_revisions(*args, **kwargs)


def _export_api_proxy(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    revision_number,
    fs_write=True,
    output_file=None,
    **kwargs,
):
    return Apis(
        gen_auth(username, password, mfa_secret, token, zonename), org
    ).export_api_proxy(
        name,
        revision_number,
        fs_write=True,
        output_file=output_file if output_file else f'{name}.zip',
    )


@apis.command(
    help='Outputs an API proxy revision as a ZIP formatted bundle of code and config files. This enables local configuration and development, including attachment of policies and scripts.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
@click.option(
    '-O', '--output-file', help='specify output file (defaults to API_NAME.zip)', default=None
)
def export(*args, **kwargs):
    _export_api_proxy(*args, **kwargs)


def _get_api_proxy(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Apis(gen_auth(username, password, mfa_secret, token, zonename), org)
        .get_api_proxy(name)
        .text
    )


@apis.command(
    help='Gets an API proxy by name, including a list of existing revisions of the proxy.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
def get(*args, **kwargs):
    console.echo(_get_api_proxy(*args, **kwargs))


def _list_api_proxies(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    prefix=None,
    format='json',
    **kwargs,
):
    return Apis(
        gen_auth(username, password, mfa_secret, token, zonename), org
    ).list_api_proxies(prefix=prefix)


@apis.command(
    help='Gets the names of all API proxies in an organization. The names correspond to the names defined in the configuration files for each API proxy.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@common_prefix_options
def list(*args, **kwargs):
    console.echo(_list_api_proxies(*args, **kwargs))


def _list_api_proxy_revisions(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Apis(gen_auth(username, password, mfa_secret, token, zonename), org)
        .list_api_proxy_revisions(name)
        .text
    )


@apis.command(help='List all revisions for an API proxy.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
def list_revisions(*args, **kwargs):
    console.echo(_list_api_proxy_revisions(*args, **kwargs))


def _undeploy_api_proxy_revision(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    revision_number,
    **kwargs,
):
    return (
        Apis(gen_auth(username, password, mfa_secret, token, zonename), org)
        .undeploy_api_proxy_revision(name, environment, revision_number)
        .text
    )


@apis.command(help='Undeploys an API proxy revision from an environment.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
def undeploy_revision(*args, **kwargs):
    console.echo(_undeploy_api_proxy_revision(*args, **kwargs))


def _force_undeploy_api_proxy_revision(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    revision_number,
    **kwargs,
):
    return (
        Apis(gen_auth(username, password, mfa_secret, token, zonename), org)
        .force_undeploy_api_proxy_revision(name, environment, revision_number)
        .text
    )


@apis.command(help='Force the undeployment of the API proxy that is partially deployed.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
def force_undeploy_revision(*args, **kwargs):
    console.echo(_force_undeploy_api_proxy_revision(*args, **kwargs))


def _pull(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    revision_number,
    environment,
    work_tree,
    dependencies=[],
    force=False,
    prefix=None,
    basepath=None,
    **kwargs,
):
    return Apis(
        gen_auth(username, password, mfa_secret, token, zonename),
        org,
        revision_number,
        environment,
        work_tree=work_tree,
    ).pull(name, force=force, prefix=prefix, basepath=basepath)


@apis.command(
    help='Downloads an API proxy revision, along with any referenced key/value maps, target servers and caches into the current working directory.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option(
    '--work-tree',
    help='set the path to the working tree (defaults to current working directory)',
)
@click.option('--force/--no-force', '-f/-F', default=False, help='force write files')
@click.option(
    '--prefix',
    help='prefix to prepend to names. WARNING: this is not foolproof. make sure to review the changes.',
)
@click.option('-b', '--basepath', help='set default basepath in apiproxy/proxies/default.xml')
def pull(*args, **kwargs):
    _pull(*args, **kwargs)


def _deploy(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    directory,
    import_only,
    seamless_deploy,
    environment,
    **kwargs,
):
    return deploy_tool(
        Struct(
            username=username,
            password=password,
            directory=directory,
            org=org,
            name=name,
            environment=environment,
            import_only=import_only,
            seamless_deploy=seamless_deploy,
            mfa_secret=mfa_secret,
            token=token,
            zonename=zonename,
        )
    )


@apis.command(
    help="""Deploy APIs using an improved version of the Apigee API Proxy Deploy Tool: https://github.com/apigee/api-platform-samples/tree/master/tools

\b
   =========================================================================
   ==  NOTICE file corresponding to the section 4 d of                    ==
   ==  the Apache License, Version 2.0,                                   ==
   ==  in this case for the Apigee API Proxy Deploy Tool code.            ==
   =========================================================================

Apigee API Proxy Deploy Tool
https://github.com/apigee/api-platform-samples/tree/master/tools
These files are Copyright 2015 Apigee Corporation, released under the Apache2 License.
"""
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-n', '--name', help='name', required=True)
@click.option(
    '-d',
    '--directory',
    help='directory with the apiproxy/ bundle',
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=False),
    required=True,
)
@optgroup.group(
    'Deployment options', cls=MutuallyExclusiveOptionGroup, help='The deployment options'
)
@optgroup.option(
    '--import-only/--no-import-only', '-i/-I', default=False, help='import only and not deploy'
)
@optgroup.option(
    '--seamless-deploy/--no-seamless-deploy',
    '-s/-S',
    default=False,
    help='seamless deploy the bundle',
)
def deploy(*args, **kwargs):
    _deploy(*args, **kwargs)
