import json
import sys

import requests
from requests.exceptions import HTTPError
from tqdm import tqdm

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.encryption_utils import (ENCRYPTED_HEADER_BEGIN, ENCRYPTED_HEADER_END,
                           decrypt_message_with_gpg, encrypt_message_with_gpg, has_encrypted_header)
from apigee.keyvaluemaps.serializer import KeyvaluemapsSerializer
from apigee.utils import read_file_content

CREATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps"
DELETE_KEYVALUEMAP_FROM_AN_ENVIRONMENT_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}"
DELETE_KEYVALUEMAP_ENTRY_IN_AN_ENVIRONMENT_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}"
GET_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}"
GET_A_KEYS_VALUE_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}"
LIST_KEYVALUEMAPS_IN_AN_ENVIRONMENT_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps"
UPDATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}"
CREATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries"
UPDATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}"
LIST_KEYS_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/keys?startkey={startkey}&count={count}"


def get_tqdm_kwargs(desc):
    return {
        "desc": desc,
        "unit": "entries",
        "bar_format": "{l_bar}{bar:32}{r_bar}{bar:-10b}",
        "leave": False,
    }


class Keyvaluemaps:
    def __init__(self, auth, org_name, map_name):
        self.auth = auth
        self.org_name = org_name
        self.map_name = map_name

    def create_an_entry_in_an_environment_scoped_kvm(
        self, environment, entry_name, entry_value
    ):  # sourcery skip: class-extract-method
        uri = CREATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            name=self.map_name,
        )
        resp = requests.post(uri, headers=auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        ), json={"name": entry_name, "value": entry_value})
        resp.raise_for_status()
        return resp

    def create_keyvaluemap_in_an_environment(self, environment, request_body):
        uri = CREATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, environment=environment
        )
        resp = requests.post(uri, headers=auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        ), json=json.loads(request_body))
        resp.raise_for_status()
        return resp

    def create_or_update_entry(self, environment, entry):
        try:
            self.update_an_entry_in_an_environment_scoped_kvm(
                environment, entry["name"], entry["value"]
            )
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            self.create_an_entry_in_an_environment_scoped_kvm(
                environment, entry["name"], entry["value"]
            )

    @staticmethod
    def decrypt_keyvaluemap(kvm_dict, secret):
        secret_count = 0
        if not kvm_dict["entry"]:
            return kvm_dict, secret_count
        for index, entry in enumerate(kvm_dict["entry"]):
            if entry.get("name") and entry.get("value"):
                secret_count += Keyvaluemaps.decrypt_value(kvm_dict, index, secret)
        return kvm_dict, secret_count

    @staticmethod
    def decrypt_value(kvm_dict, entry_index, secret):
        ciphertext = kvm_dict["entry"][entry_index]["value"]
        if not has_encrypted_header(ciphertext):
            return 0
        decrypted_value = decrypt_message_with_gpg(secret, ciphertext)
        if decrypted_value == "":
            sys.exit("Incorrect symmetric key.")
        kvm_dict["entry"][entry_index]["value"] = decrypted_value
        return 1

    def delete_entries(self, environment, entries_to_delete):
        for entry in tqdm(entries_to_delete, **get_tqdm_kwargs("Deleting")):
            self.delete_keyvaluemap_entry_in_an_environment(environment, entry["name"])

    def delete_keyvaluemap_entry_in_an_environment(self, environment, entry_name):
        uri = DELETE_KEYVALUEMAP_ENTRY_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            name=self.map_name,
            entry_name=entry_name,
        )
        return self.send_delete_request(uri)

    def delete_keyvaluemap_from_an_environment(self, environment):
        uri = DELETE_KEYVALUEMAP_FROM_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            name=self.map_name,
        )
        return self.send_delete_request(uri)

    @staticmethod
    def encrypt_keyvaluemap(kvm_dict, secret):
        secret_count = 0
        if not kvm_dict["entry"]:
            return kvm_dict, secret_count
        for index, entry in enumerate(kvm_dict["entry"]):
            if entry.get("name") and entry.get("value"):
                secret_count += Keyvaluemaps.encrypt_value(kvm_dict, index, secret)
        return kvm_dict, secret_count

    @staticmethod
    def encrypt_value(kvm_dict, entry_index, secret):
        plaintext = kvm_dict["entry"][entry_index]["value"]
        if has_encrypted_header(plaintext):
            return 0
        encrypted_value = f"{ENCRYPTED_HEADER_BEGIN}{encrypt_message_with_gpg(secret, plaintext)}{ENCRYPTED_HEADER_END}"
        kvm_dict["entry"][entry_index]["value"] = encrypted_value
        return 1

    def fetch_keys_in_environment_scoped_keyvaluemap(self, uri):
        result = requests.get(uri, headers=auth.set_authentication_headers(
            self.auth, custom_headers={"Accept": "application/json"}
        ))
        result.raise_for_status()
        return result

    @staticmethod
    def find_deleted_keys(kvm_dict1, kvm_dict2):
        return [
            entry
            for entry in kvm_dict2["entry"]
            if entry["name"] not in {entry["name"] for entry in kvm_dict1["entry"]}
        ]

    def get_a_keys_value_in_an_environment_scoped_keyvaluemap(
        self, environment, entry_name
    ):
        uri = GET_A_KEYS_VALUE_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            name=self.map_name,
            entry_name=entry_name,
        )
        return self.fetch_keys_in_environment_scoped_keyvaluemap(uri)

    def get_keyvaluemap_in_an_environment(self, environment):
        uri = GET_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            name=self.map_name,
        )
        return self.fetch_keys_in_environment_scoped_keyvaluemap(uri)

    def list_keys_in_an_environment_scoped_keyvaluemap(
        self, environment, startkey, count
    ):
        uri = LIST_KEYS_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            name=self.map_name,
            startkey=startkey,
            count=count,
        )
        return self.fetch_keys_in_environment_scoped_keyvaluemap(uri)

    def list_keyvaluemaps_in_an_environment(
        self, environment, prefix=None, format="json"
    ):
        uri = LIST_KEYVALUEMAPS_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, environment=environment
        )
        resp = (
            self.fetch_keys_in_environment_scoped_keyvaluemap(
                uri
            )
        )
        return KeyvaluemapsSerializer().serialize_details(resp, format, prefix=prefix)

    def push_keyvaluemap(self, environment, file, secret=None):
        local_map = read_file_content(file, type="json")
        if secret:
            console.echo("Decrypting... ", line_ending="", should_flush=True)
            local_map, decrypted_count = Keyvaluemaps.decrypt_keyvaluemap(
                local_map, secret
            )
            if decrypted_count:
                console.echo("Done.")
            else:
                console.echo("Nothing to decrypt.")
        elif any(has_encrypted_header(entry.get("value")) for entry in local_map["entry"]):
            sys.exit(
                "KVM appears to be encrypted but no symmetric key (secret) was specified."
            )
        self.map_name = local_map["name"]
        try:
            self.synchronize_keyvaluemap_with_environment(environment, local_map)
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            console.echo(f"Creating {self.map_name}")
            console.echo(
                self.create_keyvaluemap_in_an_environment(
                    environment, json.dumps(local_map)
                ).text
            )

    def send_delete_request(self, uri):
        resp = requests.delete(uri, headers=auth.set_authentication_headers(
            self.auth, custom_headers={"Accept": "application/json"}
        ))
        resp.raise_for_status()
        return resp

    def synchronize_keyvaluemap_with_environment(self, environment, local_map):
        """
        Synchronizes the local Key-Value Map (KVM) with the specified environment.

        This method compares the entries in the local_map with the existing Key-Value Map in the given environment.
        It performs the following actions to synchronize the KVM:
        - Removes any entries in the environment's KVM that are not present in the local_map.
        - Updates the entries in the environment's KVM with the ones from the local_map that have different values.
        - Creates new entries in the environment's KVM for the entries in the local_map that are not already present.

        Args:
            environment (str): The name of the environment where the KVM should be synchronized.
            local_map (dict): The local Key-Value Map (KVM) containing the entries to synchronize.

        Raises:
            Exception: If there is an error during the synchronization process.

        Returns:
            None: The method does not return a value directly. It performs the necessary synchronization actions.
        """
        remote_map = self.get_keyvaluemap_in_an_environment(environment).json()
        deleted_keys = Keyvaluemaps.find_deleted_keys(local_map, remote_map)
        entries_to_update = {
            "entry": [
                entry
                for entry in local_map["entry"]
                if entry not in remote_map["entry"]
            ]
        }
        if deleted_keys:
            self.delete_entries(environment, deleted_keys)
            console.echo("Removed entries.")
        if entries_to_update["entry"]:
            for entry in tqdm(
                entries_to_update["entry"], **get_tqdm_kwargs("Updating")
            ):
                self.create_or_update_entry(environment, entry)
            console.echo("Updated entries.")
        if not deleted_keys and not entries_to_update["entry"]:
            console.echo("All entries up-to-date.")

    def update_an_entry_in_an_environment_scoped_kvm(
        self, environment, entry_name, updated_value
    ):
        uri = UPDATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            name=self.map_name,
            entry_name=entry_name,
        )
        resp = requests.post(uri, headers=auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        ), json={"name": entry_name, "value": updated_value})
        resp.raise_for_status()
        return resp

    def update_keyvaluemap_in_an_environment(self, environment, request_body):
        uri = UPDATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            name=self.map_name,
        )
        resp = requests.post(uri, headers=auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        ), json=json.loads(request_body))
        resp.raise_for_status()
        return resp
