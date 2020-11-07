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
    '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps'
)
DELETE_KEYVALUEMAP_FROM_AN_ENVIRONMENT_PATH = (
    '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}'
)
DELETE_KEYVALUEMAP_ENTRY_IN_AN_ENVIRONMENT_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}'
GET_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH = (
    '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}'
)
GET_A_KEYS_VALUE_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}'
LIST_KEYVALUEMAPS_IN_AN_ENVIRONMENT_PATH = (
    '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps'
)
UPDATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH = (
    '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}'
)
CREATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH = (
    '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries'
)
UPDATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/entries/{entry_name}'
LIST_KEYS_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/keyvaluemaps/{name}/keys?startkey={startkey}&count={count}'


def TQDM_KWARGS(desc):
    return {
        'desc': desc,
        'unit': 'entries',
        'bar_format': '{l_bar}{bar:32}{r_bar}{bar:-10b}',
        'leave': False,
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

    def create_keyvaluemap_in_an_environment(self, environment, request_body):
        uri = CREATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment
        )
        hdrs = auth.set_header(
            self._auth, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_keyvaluemap_from_an_environment(self, environment):
        uri = DELETE_KEYVALUEMAP_FROM_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_keyvaluemap_entry_in_an_environment(self, environment, entry_name):
        uri = DELETE_KEYVALUEMAP_ENTRY_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
            entry_name=entry_name,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
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
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_a_keys_value_in_an_environment_scoped_keyvaluemap(self, environment, entry_name):
        uri = GET_A_KEYS_VALUE_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
            entry_name=entry_name,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_keyvaluemaps_in_an_environment(self, environment, prefix=None, format='json'):
        uri = LIST_KEYVALUEMAPS_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, environment=environment
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return KeyvaluemapsSerializer().serialize_details(resp, format, prefix=prefix)

    def update_keyvaluemap_in_an_environment(self, environment, request_body):
        uri = UPDATE_KEYVALUEMAP_IN_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
        )
        hdrs = auth.set_header(
            self._auth, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def create_an_entry_in_an_environment_scoped_kvm(self, environment, entry_name, entry_value):
        uri = CREATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
        )
        hdrs = auth.set_header(
            self._auth, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}
        )
        body = {'name': entry_name, 'value': entry_value}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def update_an_entry_in_an_environment_scoped_kvm(self, environment, entry_name, updated_value):
        uri = UPDATE_AN_ENTRY_IN_AN_ENVIRONMENT_SCOPED_KVM_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
            entry_name=entry_name,
        )
        hdrs = auth.set_header(
            self._auth, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}
        )
        body = {'name': entry_name, 'value': updated_value}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def list_keys_in_an_environment_scoped_keyvaluemap(self, environment, startkey, count):
        uri = LIST_KEYS_IN_AN_ENVIRONMENT_SCOPED_KEYVALUEMAP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            name=self._map_name,
            startkey=startkey,
            count=count,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        # return KeyvaluemapsSerializer().serialize_details(resp, 'json', prefix=prefix)
        return resp

    def _diff_kvms(self, kvm1, kvm2):
        current_keys = [entry['name'] for entry in kvm1['entry']]
        deleted_keys = [entry for entry in kvm2['entry'] if entry['name'] not in current_keys]
        return current_keys, deleted_keys

    def _create_or_update_entry(self, environment, entry):
        try:
            self.get_a_keys_value_in_an_environment_scoped_keyvaluemap(environment, entry['name'])
            self.update_an_entry_in_an_environment_scoped_kvm(
                environment, entry['name'], entry['value']
            )
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            self.create_an_entry_in_an_environment_scoped_kvm(
                environment, entry['name'], entry['value']
            )

    def _delete_entries(self, environment, deleted_keys):
        for idx, entry in enumerate(tqdm(deleted_keys, **TQDM_KWARGS('Deleting'))):
            self.delete_keyvaluemap_entry_in_an_environment(environment, entry['name'])

    @staticmethod
    def encrypt_value(kvm_dict, index, secret):
        plaintext = kvm_dict['entry'][index]['value']
        kvm_dict['entry'][index][
            'value'
        ] = f'{ENCRYPTED_HEADER_BEGIN}{encrypt_message(secret, plaintext)}{ENCRYPTED_HEADER_END}'

    @staticmethod
    def decrypt_value(kvm_dict, index, secret):
        ciphertext = kvm_dict['entry'][index]['value']
        decrypted = decrypt_message(secret, ciphertext)
        if decrypted == '':
            sys.exit('Incorrect symmetric key.')
        kvm_dict['entry'][index]['value'] = decrypted

    @staticmethod
    def encrypt_decrypt_keyvaluemap(kvm_dict, secret, encrypt=True):
        crypto_count = 0

        def _func(value, kvm, index, secret):
            operation = ''
            if encrypt:
                operation = 'encrypt_value' if not is_encrypted(value) else ''
            else:
                operation = 'decrypt_value' if is_encrypted(value) else ''
            if operation:
                getattr(Keyvaluemaps, operation)(kvm, index, secret)
                return 1
            return 0

        if kvm_dict['encrypted'] and kvm_dict['entry']:
            for idx, entry in enumerate(kvm_dict['entry']):
                if entry.get('name') and entry.get('value'):
                    crypto_count += _func(kvm_dict['entry'][idx]['value'], kvm_dict, idx, secret)
        return kvm_dict, crypto_count

    def push_keyvaluemap(self, environment, file, secret=None):
        local_map = read_file(file, type='json')
        if secret:
            console.echo('Decrypting... ', end='', flush=True)
            local_map, decrypted_count = self.encrypt_decrypt_keyvaluemap(
                local_map, secret, encrypt=False
            )
            if decrypted_count:
                console.echo('Done')
            else:
                console.echo('None')
        self._map_name = local_map['name']
        try:
            remote_map = self.get_keyvaluemap_in_an_environment(environment).json()
            _, deleted_keys = self._diff_kvms(local_map, remote_map)
            local_map_updated = {
                'entry': [entry for entry in local_map['entry'] if entry not in remote_map['entry']]
            }
            if deleted_keys:
                self._delete_entries(environment, deleted_keys)
                console.echo('Removed entries.')
            if local_map_updated['entry']:
                for entry in tqdm(local_map_updated['entry'], **TQDM_KWARGS('Updating')):
                    self._create_or_update_entry(environment, entry)
                console.echo('Updated entries.')
            if not deleted_keys and not local_map_updated['entry']:
                console.echo('All entries up-to-date.')
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            console.echo(f'Creating {self._map_name}')
            console.echo(
                self.create_keyvaluemap_in_an_environment(environment, json.dumps(local_map)).text
            )
