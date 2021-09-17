import json
import sys

from apigee.crypto import (ENCRYPTED_HEADER_BEGIN, ENCRYPTED_HEADER_END,
                           decrypt_message, encrypt_message, is_encrypted)


class KeyvaluemapsSerializer:
    def diff_kvms(self, kvm1, kvm2):
        current_keys = [entry['name'] for entry in kvm1['entry']]
        deleted_keys = [entry for entry in kvm2['entry'] if entry['name'] not in current_keys]
        return current_keys, deleted_keys

    def encrypt_decrypt_keyvaluemap(self, kvm_dict, secret, encrypt=True):
        crypto_count = 0

        def _func(value, kvm, index, secret):
            operation = ''
            if encrypt:
                operation = 'encrypt_value' if not is_encrypted(value) else ''
            else:
                operation = 'decrypt_value' if is_encrypted(value) else ''
            if operation:
                getattr(KeyvaluemapsSerializer(), operation)(kvm, index, secret)
                return 1
            return 0

        if kvm_dict['encrypted'] and kvm_dict['entry']:
            for idx, entry in enumerate(kvm_dict['entry']):
                if entry.get('name') and entry.get('value'):
                    crypto_count += _func(kvm_dict['entry'][idx]['value'], kvm_dict, idx, secret)
        return kvm_dict, crypto_count

    def encrypt_value(self, kvm_dict, index, secret):
        plaintext = kvm_dict['entry'][index]['value']
        kvm_dict['entry'][index][
            'value'
        ] = f'{ENCRYPTED_HEADER_BEGIN}{encrypt_message(secret, plaintext)}{ENCRYPTED_HEADER_END}'

    def decrypt_value(self, kvm_dict, index, secret):
        ciphertext = kvm_dict['entry'][index]['value']
        decrypted = decrypt_message(secret, ciphertext)
        if decrypted == '':
            sys.exit('Incorrect symmetric key.')
        kvm_dict['entry'][index]['value'] = decrypted

    def serialize_details(self, maps, format, prefix=None):
        resp = maps
        if format == 'text':
            return maps.text
        maps = maps.json()
        if prefix:
            maps = [map for map in maps if map.startswith(prefix)]
        if format == 'json':
            return json.dumps(maps)
        elif format == 'table':
            pass
        elif format == 'dict':
            return maps
        return resp
