import click
from click_option_group import RequiredMutuallyExclusiveOptionGroup, optgroup

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.prefix import common_prefix_options
from apigee.sharedflows.sharedflows import Sharedflows
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options


@click.group(help='You can use the following APIs to manage shared flows and flow hooks.')
def sharedflows():
    pass


def _get_a_list_of_shared_flows(
    username, password, mfa_secret, token, zonename, org, profile, prefix=None, **kwargs
):
    return Sharedflows(
        gen_auth(username, password, mfa_secret, token, zonename), org
    ).get_a_list_of_shared_flows(prefix=prefix)


@sharedflows.command(
    help='Gets an array of the names of shared flows in the organization. The response is a simple array of strings.'
)
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
def list(*args, **kwargs):
    console.echo(_get_a_list_of_shared_flows(*args, **kwargs))


def _import_a_shared_flow(
    username, password, mfa_secret, token, zonename, org, profile, file, name, **kwargs
):
    return (
        Sharedflows(gen_auth(username, password, mfa_secret, token, zonename), org)
        .import_a_shared_flow(file, name)
        .text
    )


@sharedflows.command(
    name='import',
    help='Uploads a ZIP-formatted shared flow configuration bundle from a local machine to an Edge organization. If the shared flow already exists, this creates a new revision of it. If the shared flow does not exist, this creates it. Once imported, the shared flow revision must be deployed before it can be accessed at runtime. By default, shared flow configurations are not validated on import.',
)
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option(
    '-f',
    '--file',
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    required=True,
    help='file path of the shared flow configuration in ZIP format',
)
@click.option('-n', '--name', help='name', required=True)
def import_a_shared_flow(*args, **kwargs):
    console.echo(_import_a_shared_flow(*args, **kwargs))


# def _export_a_shared_flow(self, shared_flow_name, revision_number):
#     pass


def _get_a_shared_flow(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Sharedflows(gen_auth(username, password, mfa_secret, token, zonename), org)
        .get_a_shared_flow(name)
        .text
    )


@sharedflows.command(help='Gets a shared flow by name, including a list of its revisions.')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
def get(*args, **kwargs):
    console.echo(_get_a_shared_flow(*args, **kwargs))


def _deploy_a_shared_flow(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    environment,
    name,
    revision_number,
    override,
    delay,
    file,
    **kwargs
):
    return (
        Sharedflows(gen_auth(username, password, mfa_secret, token, zonename), org)
        .deploy_a_shared_flow(
            environment,
            name,
            revision_number,
            override=override,
            delay=delay,
            shared_flow_file=file,
        )
        .text
    )


@sharedflows.command(
    help='Deploys a shared flow revision to an environment in an organization. Shared flows cannot be used until they have been deployed to an environment. If you experience HTTP 500 errors during deployment, consider using the override parameter to deploy the shared flow in place of a revision currently deployed. The size limit of a shared flow bundle is 15 MB. WARNING: currently, --override does not seem to work on Apigee Edge. To counter this, existing shared flow revisions in the target environment will be undeployed before deploying a new revision, resulting in some downtime.'
)
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-n', '--name', help='name', required=True)
@optgroup.group(
    'Deployment options',
    cls=RequiredMutuallyExclusiveOptionGroup,
    help='The deployment options',
)
@optgroup.option(
    '-f',
    '--file',
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    help='file path of the shared flow configuration in ZIP format',
)
@optgroup.option('-r', '--revision-number', type=click.INT, help='revision number')
@click.option(
    '--override/--no-override',
    default=False,
    show_default=True,
    help='Set this flag to "true" to deploy the shared flow revision in place of the revision currently deployed (also known as "zero downtime" deployment).',
)
@click.option(
    '--delay',
    type=click.INT,
    default=0,
    show_default=True,
    help='Enforces a delay, measured in seconds, before the currently deployed API proxy revision is undeployed and replaced by the new revision that is being deployed. Use this setting to minimize the impact of deployment on in-flight transactions. The default value is 0.',
)
def deploy(*args, **kwargs):
    console.echo(_deploy_a_shared_flow(*args, **kwargs))


def _undeploy_a_shared_flow(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    environment,
    name,
    revision_number,
    **kwargs
):
    return (
        Sharedflows(gen_auth(username, password, mfa_secret, token, zonename), org)
        .undeploy_a_shared_flow(environment, name, revision_number)
        .text
    )


@sharedflows.command(help='Undeploys a shared flow revision from an environment.')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-n', '--name', help='name', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
def undeploy(*args, **kwargs):
    console.echo(_undeploy_a_shared_flow(*args, **kwargs))


def _get_deployment_environments_for_shared_flows(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    revision_number,
    **kwargs
):
    return (
        Sharedflows(gen_auth(username, password, mfa_secret, token, zonename), org)
        .get_deployment_environments_for_shared_flows(name, revision_number)
        .text
    )


@sharedflows.command(
    help='Gets an array of the environments to which the shared flow is deployed.'
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
def get_deployment_environments(*args, **kwargs):
    console.echo(_get_deployment_environments_for_shared_flows(*args, **kwargs))


def _delete_a_shared_flow(self, shared_flow_name):
    pass


# def _attach_a_shared_flow_to_a_flow_hook(self, environment, flow_hook, request_body):
#     pass
#
# def _detaches_a_shared_flow_from_a_flow_hook(self, environment, flow_hook):
#     pass


def _get_the_shared_flow_attached_to_a_flow_hook(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    environment,
    flow_hook,
    **kwargs
):
    return (
        Sharedflows(gen_auth(username, password, mfa_secret, token, zonename), org)
        .get_the_shared_flow_attached_to_a_flow_hook(environment, flow_hook)
        .text
    )


@sharedflows.command(
    help="Returns the name of the shared flow attached to the specified flow hook. If there's no shared flow attached to the flow hook, the API does not return an error; it simply does not return a name in the response. Specify one of these flowhook locations in the API: PreProxyFlowHook, PreTargetFlowHook, PostTargetFlowHook, PostProxyFlowHook."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-e', '--environment', help='environment', required=True)
@click.option(
    '--flow-hook', help='flow hook to which the shared flow is attached', required=True
)
def get_flow_hook(*args, **kwargs):
    console.echo(_get_the_shared_flow_attached_to_a_flow_hook(*args, **kwargs))


def _get_shared_flow_deployments(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Sharedflows(gen_auth(username, password, mfa_secret, token, zonename), org)
        .get_shared_flow_deployments(name)
        .text
    )


@sharedflows.command(help='View all shared flow deployments.')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
def get_deployments(*args, **kwargs):
    console.echo(_get_shared_flow_deployments(*args, **kwargs))


def _get_shared_flow_revisions(
    username, password, mfa_secret, token, zonename, org, profile, name, **kwargs
):
    return (
        Sharedflows(gen_auth(username, password, mfa_secret, token, zonename), org)
        .get_shared_flow_revisions(name)
        .text
    )


@sharedflows.command(help='List the revisions of a shared flow.')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
def get_revisions(*args, **kwargs):
    console.echo(_get_shared_flow_revisions(*args, **kwargs))
