import click

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.keystores.keystores import Keystores
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options


@click.group(
    help="A list of URIs used to create, modify, and delete keystores and truststores."
)
def keystores():
    pass


def _create_a_keystore_or_truststore(*args, **kwargs):
    pass


@keystores.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def create(*args, **kwargs):
    _create_a_keystore_or_truststore(*args, **kwargs)


def _delete_a_keystore_or_truststore(*args, **kwargs):
    pass


@keystores.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def delete(*args, **kwargs):
    _delete_a_keystore_or_truststore(*args, **kwargs)


def _list_all_keystores_and_truststores(
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
    return Keystores(
        gen_auth(username, password, mfa_secret, token, zonename), org, None
    ).list_all_keystores_and_truststores(environment, prefix=prefix)


@keystores.command(
    help="Returns a list of all keystores and truststores in the environment."
)
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option("-e", "--environment", help="environment", required=True)
def list(*args, **kwargs):
    console.echo(_list_all_keystores_and_truststores(*args, **kwargs))


def _get_a_keystore_or_truststore(
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
        Keystores(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_a_keystore_or_truststore(environment)
        .text
    )


@keystores.command(help="Returns a specific keystore or truststore in the environment.")
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="keystore name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
def get(*args, **kwargs):
    console.echo(_get_a_keystore_or_truststore(*args, **kwargs))


def _test_a_keystore_or_truststore(*args, **kwargs):
    pass


@keystores.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def test(*args, **kwargs):
    _test_a_keystore_or_truststore(*args, **kwargs)


def _get_cert_details_from_a_keystore_or_truststore(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    cert_name,
    **kwargs
):
    return (
        Keystores(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_cert_details_from_a_keystore_or_truststore(environment, cert_name)
        .text
    )


@keystores.command(help="Returns a specific cert from a keystore or truststore.")
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="keystore name", required=True)
@click.option("--cert-name", help="cert name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
def get_cert(*args, **kwargs):
    console.echo(_get_cert_details_from_a_keystore_or_truststore(*args, **kwargs))


def _get_all_certs_from_a_keystore_or_truststore(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    prefix=None,
    **kwargs
):
    return Keystores(
        gen_auth(username, password, mfa_secret, token, zonename), org, name
    ).get_all_certs_from_a_keystore_or_truststore(environment, prefix=prefix)


@keystores.command(help="Returns all certs from a keystore or truststore.")
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="keystore name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
def get_all_certs(*args, **kwargs):
    console.echo(_get_all_certs_from_a_keystore_or_truststore(*args, **kwargs))


def _delete_cert_from_a_keystore_or_truststore(*args, **kwargs):
    pass


@keystores.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def delete_cert(*args, **kwargs):
    _delete_cert_from_a_keystore_or_truststore(*args, **kwargs)


def _export_a_cert(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    cert_name,
    **kwargs
):
    return (
        Keystores(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .export_a_cert(environment, cert_name)
        .text
    )


@keystores.command(help="Export a cert from a keystore or truststore.")
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="keystore name", required=True)
@click.option("--cert-name", help="cert name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
def export(*args, **kwargs):
    console.echo(_export_a_cert(*args, **kwargs))


def _upload_a_certificate_to_a_truststore(*args, **kwargs):
    pass


@keystores.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def upload_cert_to_truststore(*args, **kwargs):
    _upload_a_certificate_to_a_truststore(*args, **kwargs)


def _upload_a_jar_file_to_a_keystore(*args, **kwargs):
    pass


@keystores.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def upload_jar_to_keystore(*args, **kwargs):
    _upload_a_jar_file_to_a_keystore(*args, **kwargs)


def _create_an_alias_by_generating_a_self_signed_certificate(*args, **kwargs):
    pass


@keystores.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def create_alias(*args, **kwargs):
    _create_an_alias_by_generating_a_self_signed_certificate(*args, **kwargs)


def _list_aliases(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    prefix=None,
    **kwargs
):
    return Keystores(
        gen_auth(username, password, mfa_secret, token, zonename), org, name
    ).list_aliases(environment, prefix=prefix)


@keystores.command(help="Returns a list of all the aliases in the keystore.")
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="keystore name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
def list_aliases(*args, **kwargs):
    console.echo(_list_aliases(*args, **kwargs))


def _get_alias(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    alias_name,
    **kwargs
):
    return (
        Keystores(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .get_alias(environment, alias_name)
        .text
    )


@keystores.command(help="Returns details about an alias.")
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="keystore name", required=True)
@click.option("--alias-name", help="alias name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
def get_alias(*args, **kwargs):
    console.echo(_get_alias(*args, **kwargs))


def _update_the_certificate_in_an_alias(*args, **kwargs):
    pass


@keystores.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def update_cert_in_alias(*args, **kwargs):
    _update_the_certificate_in_an_alias(*args, **kwargs)


def _generate_a_csr_for_an_alias(*args, **kwargs):
    pass


@keystores.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def generate_csr_for_alias(*args, **kwargs):
    _generate_a_csr_for_an_alias(*args, **kwargs)


def _export_a_certificate_for_an_alias(
    username,
    password,
    mfa_secret,
    token,
    zonename,
    org,
    profile,
    name,
    environment,
    alias_name,
    **kwargs
):
    return (
        Keystores(gen_auth(username, password, mfa_secret, token, zonename), org, name)
        .export_a_certificate_for_an_alias(environment, alias_name)
        .text
    )


@keystores.command(
    help="Exports a certificate or certificate chain for the specified alias in a keystore."
)
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="keystore name", required=True)
@click.option("--alias-name", help="alias name", required=True)
@click.option("-e", "--environment", help="environment", required=True)
def export_cert_for_alias(*args, **kwargs):
    console.echo(_export_a_certificate_for_an_alias(*args, **kwargs))


def _delete_alias(*args, **kwargs):
    pass


@keystores.command(help="")
@common_auth_options
@common_silent_options
@common_verbose_options
def delete_alias(*args, **kwargs):
    _delete_alias(*args, **kwargs)
