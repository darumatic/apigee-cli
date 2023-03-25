import json
import sys

import requests
from requests.exceptions import HTTPError
from tqdm import tqdm

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.crypto import (ENCRYPTED_HEADER_BEGIN, ENCRYPTED_HEADER_END,
                           decrypt_message, encrypt_message, is_encrypted)
from apigee.keyvaluemaps.serializer import KeyvaluemapsSerializer
from apigee.utils import read_file

CREATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH = (
    "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps"
)
DELETE_KEYVALUEMAP_FROM_AN_ENVIRONMENT_PATH = (
    "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}"
)
DELETE_KEYVALUEMAP_ENTRY_IN_AN_ENVIRONMENT_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}"
GET_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH = (
    "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}"
)
GET_A_KEYS_VALUE_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}"
LIST_KEYVALUEMAPS_IN_AN_ENVIRONMENT_PATH = (
    "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps"
)
UPDATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH = (
    "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}"
)
CREATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries"
UPDATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}"
LIST_KEYS_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/keys?startkey={startkey}&count={count}"


def TQDM_KWARGS(desc):
    return {
        "desc": desc,
        "unit": "entries",
        "bar_format": "{l_bar}{bar:32}{r_bar}{bar:-10b}",
        "leave": False,
    }


class Keyvaluemaps:
    def __init__(self, auth, org_name, map_name):
        self._auth = auth
        self._org_name = org_name
        self._map_name = map_name

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
    def map_name(self):
        return self._map_name

    @map_name.setter
    def map_name(self, value):
        self._map_name = value

    @staticmethod
    def find_deleted_keys(kvm1, kvm2):
        return [
            entry
            for entry in kvm2["entry"]
            if entry["name"] not in {entry["name"] for entry in kvm1["entry"]}
        ]

    @staticmethod
    def encrypt_value(kvm_dict, index, secret):
        plaintext = kvm_dict["entry"][index]["value"]
        if is_encrypted(plaintext):
            return 0
        kvm_dict["entry"][index][
            "value"
        ] = f"{ENCRYPTED_HEADER_BEGIN}{encrypt_message(secret, plaintext)}{ENCRYPTED_HEADER_END}"
        return 1

    @staticmethod
    def decrypt_value(kvm_dict, index, secret):
        ciphertext = kvm_dict["entry"][index]["value"]
        if not is_encrypted(ciphertext):
            return 0
        decrypted = decrypt_message(secret, ciphertext)
        if decrypted == "":
            sys.exit("Incorrect symmetric key.")
        kvm_dict["entry"][index]["value"] = decrypted
        return 1

    @staticmethod
    def encrypt_keyvaluemap(kvm_dict, secret):
        crypto_count = 0
        if not kvm_dict["entry"]:
            return kvm_dict, crypto_count
        for idx, entry in enumerate(kvm_dict["entry"]):
            if entry.get("name") and entry.get("value"):
                crypto_count += Keyvaluemaps.encrypt_value(kvm_dict, idx, secret)
        return kvm_dict, crypto_count

    @staticmethod
    def decrypt_keyvaluemap(kvm_dict, secret):
        crypto_count = 0
        if not kvm_dict["entry"]:
            return kvm_dict, crypto_count
        for idx, entry in enumerate(kvm_dict["entry"]):
            if entry.get("name") and entry.get("value"):
                crypto_count += Keyvaluemaps.decrypt_value(kvm_dict, idx, secret)
        return kvm_dict, crypto_count

    def create_keyvaluemap_in_an_environment(self, environment, request_body):
        uri = CREATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment
        )
        return self._extracted_from_update_keyvaluemap_in_an_environment_5(
            request_body, uri
        )

    def create_or_update_entry(self, environment, entry):
        try:
            self.get_a_keys_value_in_an_environment_scoped_keyvaluemap(
                environment, entry["name"]
            )
            self.update_an_entry_in_an_environment_scoped_kvm(
                environment, entry["name"], entry["value"]
            )
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            self.create_an_entry_in_an_environment_scoped_kvm(
                environment, entry["name"], entry["value"]
            )

    def delete_entries(self, environment, keys_to_be_deleted):
        for entry in tqdm(keys_to_be_deleted, **TQDM_KWARGS("Deleting")):
            self.delete_keyvaluemap_entry_in_an_environment(environment, entry["name"])

    def delete_keyvaluemap_from_an_environment(self, environment):
        uri = DELETE_KEYVALUEMAP_FROM_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
        )
        return self._extracted_from_delete_keyvaluemap_entry_in_an_environment_8(uri)

    def delete_keyvaluemap_entry_in_an_environment(self, environment, entry_name):
        uri = DELETE_KEYVALUEMAP_ENTRY_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
            entry_name=entry_name,
        )
        return self._extracted_from_delete_keyvaluemap_entry_in_an_environment_8(uri)

    # TODO Rename this here and in `delete_keyvaluemap_from_an_environment` and `delete_keyvaluemap_entry_in_an_environment`
    def _extracted_from_delete_keyvaluemap_entry_in_an_environment_8(self, uri):
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_keyvaluemap_in_an_environment(self, environment):
        uri = GET_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
        )
        return self._extracted_from_list_keys_in_an_environment_scoped_keyvaluemap_8(
            uri
        )

    def get_a_keys_value_in_an_environment_scoped_keyvaluemap(
        self, environment, entry_name
    ):
        uri = GET_A_KEYS_VALUE_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
            entry_name=entry_name,
        )
        return self._extracted_from_list_keys_in_an_environment_scoped_keyvaluemap_8(
            uri
        )

    def list_keyvaluemaps_in_an_environment(
        self, environment, prefix=None, format="json"
    ):
        uri = LIST_KEYVALUEMAPS_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment
        )
        resp = self._extracted_from_list_keys_in_an_environment_scoped_keyvaluemap_8(
            uri
        )
        return KeyvaluemapsSerializer().serialize_details(resp, format, prefix=prefix)

    def update_keyvaluemap_in_an_environment(self, environment, request_body):
        uri = UPDATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
        )
        return self._extracted_from_update_keyvaluemap_in_an_environment_5(
            request_body, uri
        )

    def _extracted_from_update_keyvaluemap_in_an_environment_5(self, request_body, uri):
        hdrs = auth.set_header(
            self._auth,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        body = json.loads(request_body)
        return self._extracted_from_update_an_entry_in_an_environment_scoped_kvm_10(
            uri, hdrs, body
        )

    def create_an_entry_in_an_environment_scoped_kvm(
        self, environment, entry_name, entry_value
    ):
        uri = CREATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
        )
        return self._extracted_from_update_an_entry_in_an_environment_scoped_kvm_10(
            entry_name, entry_value, uri
        )

    # TODO Rename this here and in `create_keyvaluemap_in_an_environment`, `update_keyvaluemap_in_an_environment`, `create_an_entry_in_an_environment_scoped_kvm` and `update_an_entry_in_an_environment_scoped_kvm`
    def update_an_entry_in_an_environment_scoped_kvm(
        self, environment, entry_name, updated_value
    ):
        uri = UPDATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
            entry_name=entry_name,
        )
        return self._extracted_from_update_an_entry_in_an_environment_scoped_kvm_10(
            entry_name, updated_value, uri
        )

    # TODO Rename this here and in `create_keyvaluemap_in_an_environment`, `update_keyvaluemap_in_an_environment`, `create_an_entry_in_an_environment_scoped_kvm` and `update_an_entry_in_an_environment_scoped_kvm`
    def _extracted_from_update_an_entry_in_an_environment_scoped_kvm_10(
        self, entry_name, arg1, uri
    ):
        hdrs = auth.set_header(
            self._auth,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        body = {"name": entry_name, "value": arg1}
        return self._extracted_from_update_an_entry_in_an_environment_scoped_kvm_10(
            uri, hdrs, body
        )

    # TODO Rename this here and in `create_keyvaluemap_in_an_environment`, `update_keyvaluemap_in_an_environment`, `create_an_entry_in_an_environment_scoped_kvm` and `update_an_entry_in_an_environment_scoped_kvm`
    def _extracted_from_update_an_entry_in_an_environment_scoped_kvm_10(
        self, uri, hdrs, body
    ):
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def list_keys_in_an_environment_scoped_keyvaluemap(
        self, environment, startkey, count
    ):
        uri = LIST_KEYS_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
            startkey=startkey,
            count=count,
        )
        return self._extracted_from_list_keys_in_an_environment_scoped_keyvaluemap_8(
            uri
        )

    # TODO Rename this here and in `get_keyvaluemap_in_an_environment`, `get_a_keys_value_in_an_environment_scoped_keyvaluemap`, `list_keyvaluemaps_in_an_environment` and `list_keys_in_an_environment_scoped_keyvaluemap`
    def _extracted_from_list_keys_in_an_environment_scoped_keyvaluemap_8(self, uri):
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        result = requests.get(uri, headers=hdrs)
        result.raise_for_status()
        return result

    def push_keyvaluemap(self, environment, file, secret=None):
        local_map = read_file(file, type="json")
        if secret:
            console.echo("Decrypting... ", end="", flush=True)
            local_map, decrypted_count = Keyvaluemaps.decrypt_keyvaluemap(
                local_map, secret
            )
            if decrypted_count:
                console.echo("Done.")
            else:
                console.echo("Nothing to decrypt.")
        elif any(is_encrypted(entry.get("value")) for entry in local_map["entry"]):
            sys.exit(
                "KVM appears to be encrypted but no symmetric key (secret) was specified."
            )
        self._map_name = local_map["name"]
        try:
            self._extracted_from_push_keyvaluemap_18(environment, local_map)
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            console.echo(f"Creating {self._map_name}")
            console.echo(
                self.create_keyvaluemap_in_an_environment(
                    environment, json.dumps(local_map)
                ).text
            )

    # TODO Rename this here and in `push_keyvaluemap`
    def _extracted_from_push_keyvaluemap_18(self, environment, local_map):
        remote_map = self.get_keyvaluemap_in_an_environment(environment).json()
        deleted_keys = Keyvaluemaps.find_deleted_keys(local_map, remote_map)
        local_map_updated = {
            "entry": [
                entry
                for entry in local_map["entry"]
                if entry not in remote_map["entry"]
            ]
        }
        if deleted_keys:
            self.delete_entries(environment, deleted_keys)
            console.echo("Removed entries.")
        if local_map_updated["entry"]:
            for entry in tqdm(local_map_updated["entry"], **TQDM_KWARGS("Updating")):
                self.create_or_update_entry(environment, entry)
            console.echo("Updated entries.")
        if not deleted_keys and not local_map_updated["entry"]:
            console.echo("All entries up-to-date.")
