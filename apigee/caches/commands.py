import click

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.caches.caches import Caches
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options


@click.group(
    help='A lightweight persistence store that can be used by policies or code executing on the Apigee Edge. To support data segregation, cache resources are scoped to environments.'
)
def caches():
    pass


def _clear_all_cache_entries(
    username, password, mfa_secret, token, zonename, org, profile, name, environment, **kwargs
):
    return (
        Caches(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .clear_all_cache_entries(environment)
        .text
    )


@caches.command(help='Clears all cache entries.')
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@common_auth_options
@common_silent_options
@common_verbose_options
def clear(*args, **kwargs):
    console.echo(_clear_all_cache_entries(*args, **kwargs))


def _clear_a_cache_entry(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    entry,
    **kwargs
):
    return (
        Caches(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .clear_a_cache_entry(environment, entry)
        .text
    )


@caches.command(
    help='Clears a cache entry, which is identified by the full CacheKey prefix and value.'
)
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('--entry', help='cache entry to clear', required=True)
@common_auth_options
@common_silent_options
@common_verbose_options
def clear_entry(*args, **kwargs):
    console.echo(_clear_a_cache_entry(*args, **kwargs))


def _create_a_cache_in_an_environment(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    body,
    **kwargs
):
    return (
        Caches(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .create_a_cache_in_an_environment(environment, body)
        .text
    )


@caches.command(
    help="Creates a cache in an environment. Caches are created per environment. For data segregation, a cache created in 'test', for example, cannot be accessed by API proxies deployed in 'prod'. The JSON object in the request body can be empty to create a cache with the default settings."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-b', '--body', help='request body', required=True)
def create(*args, **kwargs):
    console.echo(_create_a_cache_in_an_environment(*args, **kwargs))


def _get_information_about_a_cache(
    username, password, mfa_secret, token, zonename, org, profile, name, environment, **kwargs
):
    return (
        Caches(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_information_about_a_cache(environment)
        .text
    )


@caches.command(
    help='Gets information about a cache. The response might contain a property named persistent. That property is no longer used by Edge.'
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
def get(*args, **kwargs):
    console.echo(_get_information_about_a_cache(*args, **kwargs))


def _list_caches_in_an_environment(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    environment,
    prefix=None,
    **kwargs
):
    return Caches(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).list_caches_in_an_environment(environment, prefix=prefix)


@caches.command(help='List caches in an environment.')
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option('-e', '--environment', help='environment', required=True)
def list(*args, **kwargs):
    console.echo(_list_caches_in_an_environment(*args, **kwargs))


def _update_a_cache_in_an_environment(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    body,
    **kwargs
):
    return (
        Caches(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .update_a_cache_in_an_environment(environment, body)
        .text
    )


@caches.command(
    help='Updates a cache in an environment. You must specify the complete definition of the cache, including the properties that you want to change and the ones that retain their current value. Any properties omitted from the request body are reset to their default value. Use Get information about a cache to obtain an object containing the current value of all properties, then change only those that you want to update.'
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-b', '--body', help='request body', required=True)
def update(*args, **kwargs):
    console.echo(_update_a_cache_in_an_environment(*args, **kwargs))


def _delete_a_cache(
    username, password, mfa_secret, token, zonename, org, profile, name, environment, **kwargs
):
    return (
        Caches(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .delete_a_cache(environment)
        .text
    )


@caches.command(help='Deletes a cache.')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
def delete(*args, **kwargs):
    console.echo(_delete_a_cache(*args, **kwargs))


def _push_cache(
    username, password, mfa_secret, token, zonename, org, profile, environment, file, **kwargs
):
    return Caches(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).push_cache(environment, file)


@caches.command(help='Push Cache to Apigee. This will create/update a Cache.')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-e', '--environment', help='environment', required=True)
@click.option(
    '-f',
    '--file',
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    required=True,
)
def push(*args, **kwargs):
    _push_cache(*args, **kwargs)
