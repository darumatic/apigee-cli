import requests

from apigee import APIGEE_ADMIN_API_URL, auth
from apigee.keystores.serializer import KeystoresSerializer

CREATE_A_KEYSTORE_OR_TRUSTSTORE_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores"
DELETE_A_KEYSTORE_OR_TRUSTSTORE_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}"
LIST_ALL_KEYSTORES_AND_TRUSTSTORES_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores"
GET_A_KEYSTORE_OR_TRUSTSTORE_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/keystores/{keystore_name}"
TEST_A_KEYSTORE_OR_TRUSTSTORE_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/testssl"
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
        self.auth = auth
        self.org_name = org_name
        self.keystore_name = keystore_name

    def export_a_cert(self, environment, cert_name):
        uri = EXPORT_A_CERT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
            keystore_name=self.keystore_name,
            cert_name=cert_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def export_a_certificate_for_an_alias(self, environment, alias_name):
        uri = EXPORT_A_CERTIFICATE_FOR_AN_ALIAS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
            keystore_name=self.keystore_name,
            alias_name=alias_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_a_keystore_or_truststore(self, environment):
        # sourcery skip: class-extract-method
        uri = GET_A_KEYSTORE_OR_TRUSTSTORE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
            keystore_name=self.keystore_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_alias(self, environment, alias_name):
        uri = GET_ALIAS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
            keystore_name=self.keystore_name,
            alias_name=alias_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_all_certs_from_a_keystore_or_truststore(
        self, environment, prefix=None, format="json"
    ):
        uri = GET_ALL_CERTS_FROM_A_KEYSTORE_OR_TRUSTSTORE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
            keystore_name=self.keystore_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return KeystoresSerializer().serialize_details(resp, format, prefix=prefix)

    def get_cert_details_from_a_keystore_or_truststore(self, environment, cert_name):
        uri = GET_CERT_DETAILS_FROM_A_KEYSTORE_OR_TRUSTSTORE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
            keystore_name=self.keystore_name,
            cert_name=cert_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_aliases(self, environment, prefix=None, format="json"):
        uri = LIST_ALIASES_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
            keystore_name=self.keystore_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return KeystoresSerializer().serialize_details(resp, format, prefix=prefix)

    def list_all_keystores_and_truststores(
        self, environment, prefix=None, format="json"
    ):
        uri = LIST_ALL_KEYSTORES_AND_TRUSTSTORES_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return KeystoresSerializer().serialize_details(resp, format, prefix=prefix)
