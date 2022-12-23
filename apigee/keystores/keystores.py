import json

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.keystores.serializer import KeystoresSerializer

CREATE_A_KEYSTORE_OR_TRUSTSTORE_PATH = (
    "{api_url}/v1/o/{org_name}/environments/{environment}/keystores"
)
DELETE_A_KEYSTORE_OR_TRUSTSTORE_PATH = (
    "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}"
)
LIST_ALL_KEYSTORES_AND_TRUSTSTORES_PATH = (
    "{api_url}/v1/o/{org_name}/environments/{environment}/keystores"
)
GET_A_KEYSTORE_OR_TRUSTSTORE_PATH = (
    "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}"
)
TEST_A_KEYSTORE_OR_TRUSTSTORE_PATH = (
    "{api_url}/v1/o/{org_name}/environments/{environment}/testssl"
)
GET_CERT_DETAILS_FROM_A_KEYSTORE_OR_TRUSTSTORE_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/certs/{cert_name}"
GET_ALL_CERTS_FROM_A_KEYSTORE_OR_TRUSTSTORE_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/certs"
DELETE_CERT_FROM_A_KEYSTORE_OR_TRUSTSTORE_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/certs/{cert_name}"
EXPORT_A_CERT_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/certs/{cert_name}/export"
UPLOAD_A_CERTIFICATE_TO_A_TRUSTSTORE_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/certs"
UPLOAD_A_JAR_FILE_TO_A_KEYSTORE_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/keys"
CREATE_AN_ALIAS_BY_GENERATING_A_SELF_SIGNED_CERTIFICATE_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/aliases"
LIST_ALIASES_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/aliases"
GET_ALIAS_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/aliases/{alias_name}"
UPDATE_THE_CERTIFICATE_IN_AN_ALIAS_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/aliases/{alias_name}"
GENERATE_A_CSR_FOR_AN_ALIAS_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/aliases/{alias_name}/csr"
EXPORT_A_CERTIFICATE_FOR_AN_ALIAS_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/aliases/{alias_name}/certificate"
DELETE_ALIAS_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}/aliases/{alias_name}"


class Keystores:
    def __init__(self, auth, org_name, keystore_name):
        self._auth = auth
        self._org_name = org_name
        self._keystore_name = keystore_name

    def __call__(self):
        pass

    @property
    def auth(self):
        return self._auth

    @auth.setter
    def auth(self, value):
        self._auth = value

    @property
    def org_name(self):
        return self._org_name

    @org_name.setter
    def org_name(self, value):
        self._org_name = value

    @property
    def keystore_name(self):
        return self._keystore_name

    @keystore_name.setter
    def keystore_name(self, value):
        self._keystore_name = value

    def create_a_keystore_or_truststore(self):
        pass

    def delete_a_keystore_or_truststore(self):
        pass

    def list_all_keystores_and_truststores(
        self, environment, prefix=None, format="json"
    ):
        uri = LIST_ALL_KEYSTORES_AND_TRUSTSTORES_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self._org_name,
            environment=environment,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return KeystoresSerializer().serialize_details(resp, format, prefix=prefix)

    def get_a_keystore_or_truststore(self, environment):
        uri = GET_A_KEYSTORE_OR_TRUSTSTORE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self._org_name,
            environment=environment,
            keystore_name=self._keystore_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def test_a_keystore_or_truststore(self):
        pass

    def get_cert_details_from_a_keystore_or_truststore(self, environment, cert_name):
        uri = GET_CERT_DETAILS_FROM_A_KEYSTORE_OR_TRUSTSTORE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self._org_name,
            environment=environment,
            keystore_name=self._keystore_name,
            cert_name=cert_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_all_certs_from_a_keystore_or_truststore(
        self, environment, prefix=None, format="json"
    ):
        uri = GET_ALL_CERTS_FROM_A_KEYSTORE_OR_TRUSTSTORE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self._org_name,
            environment=environment,
            keystore_name=self._keystore_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return KeystoresSerializer().serialize_details(resp, format, prefix=prefix)

    def delete_cert_from_a_keystore_or_truststore(self):
        pass

    def export_a_cert(self, environment, cert_name):
        uri = EXPORT_A_CERT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self._org_name,
            environment=environment,
            keystore_name=self._keystore_name,
            cert_name=cert_name,
        )
        hdrs = auth.set_header(self._auth, headers={})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def upload_a_certificate_to_a_truststore(self):
        pass

    def upload_a_jar_file_to_a_keystore(self):
        pass

    def create_an_alias_by_generating_a_self_signed_certificate(self):
        pass

    def list_aliases(self, environment, prefix=None, format="json"):
        uri = LIST_ALIASES_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self._org_name,
            environment=environment,
            keystore_name=self._keystore_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return KeystoresSerializer().serialize_details(resp, format, prefix=prefix)

    def get_alias(self, environment, alias_name):
        uri = GET_ALIAS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self._org_name,
            environment=environment,
            keystore_name=self._keystore_name,
            alias_name=alias_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def update_the_certificate_in_an_alias(self):
        pass

    def generate_a_csr_for_an_alias(self):
        pass

    def export_a_certificate_for_an_alias(self, environment, alias_name):
        uri = EXPORT_A_CERTIFICATE_FOR_AN_ALIAS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self._org_name,
            environment=environment,
            keystore_name=self._keystore_name,
            alias_name=alias_name,
        )
        hdrs = auth.set_header(self._auth, headers={})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_alias(self):
        pass
