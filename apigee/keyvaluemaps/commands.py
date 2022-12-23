import sys

import click

from apigee import APIGEE_CLI_SYMMETRIC_KEY, console
from apigee.auth import common_auth_options, gen_auth
from apigee.crypto import (
    ENCRYPTED_HEADER_BEGIN,
    ENCRYPTED_HEADER_END,
    decrypt_message,
    encrypt_message,
    is_encrypted,
)
from apigee.keyvaluemaps.keyvaluemaps import Keyvaluemaps
from apigee.keyvaluemaps.serializer import KeyvaluemapsSerializer
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.utils import read_file, write_file
from apigee.verbose import common_verbose_options


@click.group(
    help="Key/value maps at the environment scope can be accessed by any API proxy in the environment (such as test or prod). In the management UI (APIs > Environment Configuration), key/value maps are at the environment scope."
)
def keyvaluemaps():
    pass


def _create_keyvaluemap_in_an_environment(
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
        Keyvaluemaps(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .create_keyvaluemap_in_an_environment(environment, body)
        .text
    )


@keyvaluemaps.command(help="Creates a key value map in an environment.")
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
@click.option("-b", "--body", help="request body", required=True)
def create(*args, **kwargs):
    console.echo(_create_keyvaluemap_in_an_environment(*args, **kwargs))


def _delete_keyvaluemap_from_an_environment(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    **kwargs
):
    return (
        Keyvaluemaps(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .delete_keyvaluemap_from_an_environment(environment)
        .text
    )


@keyvaluemaps.command(
    help="Deletes a key/value map and all associated entries from an environment."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
def delete(*args, **kwargs):
    console.echo(_delete_keyvaluemap_from_an_environment(*args, **kwargs))


def _delete_keyvaluemap_entry_in_an_environment(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    entry_name,
    **kwargs
):
    return (
        Keyvaluemaps(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .delete_keyvaluemap_entry_in_an_environment(environment, entry_name)
        .text
    )


@keyvaluemaps.command(
    help="Deletes a specific key/value map entry in an environment by name, along with associated entries."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
@click.option("--entry-name", help="entry name", required=True)
def delete_entry(*args, **kwargs):
    console.echo(_delete_keyvaluemap_entry_in_an_environment(*args, **kwargs))


def _get_keyvaluemap_in_an_environment(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    **kwargs
):
    return (
        Keyvaluemaps(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .get_keyvaluemap_in_an_environment(environment)
        .text
    )


@keyvaluemaps.command(
    help="Gets a KeyValueMap (KVM) in an environment by name, along with the keys and values."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
def get(*args, **kwargs):
    console.echo(_get_keyvaluemap_in_an_environment(*args, **kwargs))


def _get_a_keys_value_in_an_environment_scoped_keyvaluemap(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    entry_name,
    **kwargs
):
    return (
        Keyvaluemaps(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .get_a_keys_value_in_an_environment_scoped_keyvaluemap(environment, entry_name)
        .text
    )


@keyvaluemaps.command(
    help="Gets the value of a key in an environment-scoped KeyValueMap (KVM)."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
@click.option("--entry-name", help="entry name", required=True)
def get_value(*args, **kwargs):
    console.echo(
        _get_a_keys_value_in_an_environment_scoped_keyvaluemap(*args, **kwargs)
    )


def _list_keyvaluemaps_in_an_environment(
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
    return Keyvaluemaps(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).list_keyvaluemaps_in_an_environment(environment, prefix=prefix)


@keyvaluemaps.command(
    help="Lists the name of all key/value maps in an environment and optionally returns an expanded view of all key/value maps for the environment."
)
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option("-e", "--environment", help="environment", required=True)
def list(*args, **kwargs):
    console.echo(_list_keyvaluemaps_in_an_environment(*args, **kwargs))


def _update_keyvaluemap_in_an_environment(
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
        Keyvaluemaps(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .update_keyvaluemap_in_an_environment(environment, body)
        .text
    )


@keyvaluemaps.command(
    help="Note: This API is supported for Apigee Edge for Private Cloud only. For Apigee Edge for Public Cloud use Update an entry in an environment-scoped KVM. Updates an existing KeyValueMap in an environment. Does not override the existing map. Instead, this method updates the entries if they exist or adds them if not. It can take several minutes before the new value is visible to runtime traffic."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
@click.option("-b", "--body", help="request body", required=True)
def update(*args, **kwargs):
    console.echo(_update_keyvaluemap_in_an_environment(*args, **kwargs))


def _create_an_entry_in_an_environment_scoped_kvm(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    entry_name,
    entry_value,
    **kwargs
):
    return (
        Keyvaluemaps(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .create_an_entry_in_an_environment_scoped_kvm(
            environment, entry_name, entry_value
        )
        .text
    )


@keyvaluemaps.command(
    help="Note: This API is supported for Apigee Edge for the Public Cloud only. Creates an entry in an existing KeyValueMap scoped to an environment. A key (name) cannot be larger than 2 KB. KVM names are case sensitive."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
@click.option("--entry-name", help="entry name", required=True)
@click.option("--entry-value", help="entry value", required=True)
def create_entry(*args, **kwargs):
    console.echo(_create_an_entry_in_an_environment_scoped_kvm(*args, **kwargs))


def _update_an_entry_in_an_environment_scoped_kvm(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    entry_name,
    updated_value,
    **kwargs
):
    return (
        Keyvaluemaps(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .update_an_entry_in_an_environment_scoped_kvm(
            environment, entry_name, updated_value
        )
        .text
    )


@keyvaluemaps.command(
    help="Note: This API is supported for Apigee Edge for the Public Cloud only. Updates an entry in a KeyValueMap scoped to an environment. A key cannot be larger than 2 KB. KVM names are case sensitive. Does not override the existing map. It can take several minutes before the new value is visible to runtime traffic."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
@click.option("--entry-name", help="entry name", required=True)
@click.option("--updated-value", help="updated value", required=True)
def update_entry(*args, **kwargs):
    console.echo(_update_an_entry_in_an_environment_scoped_kvm(*args, **kwargs))


def _list_keys_in_an_environment_scoped_keyvaluemap(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    startkey,
    count,
    **kwargs
):
    return (
        Keyvaluemaps(
            gen_auth(username, password, mfa_secret, token, zonename), org, name
        )
        .list_keys_in_an_environment_scoped_keyvaluemap(environment, startkey, count)
        .text
    )


@keyvaluemaps.command(
    help="Note: This API is supported for Apigee Edge for the Public Cloud only. Lists keys in a KeyValueMap scoped to an environment. KVM names are case sensitive."
)
@common_auth_options
# @common_prefix_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
@click.option(
    "--startkey",
    default="",
    show_default=True,
    help="To filter the keys that are returned, enter the name of a key that the list will start with.",
)
@click.option(
    "--count",
    type=click.INT,
    default=100,
    show_default=True,
    help="Limits the list of keys to the number you specify, up to a maximum of 100. Use with the startkey parameter to provide more targeted filtering.",
)
# @click.option("--prefix", help="team/resource prefix filter")
def list_keys(*args, **kwargs):
    console.echo(_list_keys_in_an_environment_scoped_keyvaluemap(*args, **kwargs))


def _push_keyvaluemap(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    environment,
    file,
    symmetric_key,
    **kwargs
):
    return Keyvaluemaps(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).push_keyvaluemap(environment, file, secret=symmetric_key)


@keyvaluemaps.command(
    help="Push KeyValueMap to Apigee. This will create KeyValueMap/entries if they do not exist, update existing KeyValueMap/entries, and delete entries on Apigee that are not present in the request body."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-e", "--environment", help="environment", required=True)
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    required=True,
)
@click.option(
    "--symmetric-key",
    default=APIGEE_CLI_SYMMETRIC_KEY,
    help="symmetric secret key for decrypting",
)
def push(*args, **kwargs):
    _push_keyvaluemap(*args, **kwargs)


@keyvaluemaps.command(
    name="encrypt",
    help="Use symmetric GPG (AES256) to encrypt KVM file in a custom format.",
)
@common_silent_options
@common_verbose_options
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    required=True,
)
@click.option(
    "--symmetric-key", required=True, help="symmetric secret key for encrypting"
)
def encrypt_file(symmetric_key, file, verbose, silent):
    contents = read_file(file, type="json")
    encrypted_count = 0
    console.echo("Encrypting... ", end="", flush=True)
    contents, encrypted_count = Keyvaluemaps.encrypt_keyvaluemap(
        contents, symmetric_key
    )
    if encrypted_count:
        write_file(contents, file, indent=2)
        console.echo("Done.")
        return contents
    console.echo("Nothing to encrypt.")
    return ""


@keyvaluemaps.command(
    name="decrypt",
    help="Use symmetric GPG (AES256) to decrypt KVM file in a custom format.",
)
@common_silent_options
@common_verbose_options
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False),
    required=True,
)
@click.option(
    "--symmetric-key", required=True, help="symmetric secret key for decrypting"
)
def decrypt_file(symmetric_key, file, verbose, silent):
    contents = read_file(file, type="json")
    decrypted_count = 0
    console.echo("Decrypting... ", end="", flush=True)
    contents, decrypted_count = Keyvaluemaps.decrypt_keyvaluemap(
        contents, symmetric_key
    )
    if decrypted_count:
        write_file(contents, file, indent=2)
        console.echo("Done.")
        return contents
    console.echo("Nothing to decrypt.")
    return ""
