import base64

import gnupg

ENCRYPTED_HEADER_BEGIN = "-----BEGIN ENCRYPTED APIGEE CLI MESSAGE-----"
ENCRYPTED_HEADER_END = "-----END ENCRYPTED APIGEE CLI MESSAGE-----"


def encrypt_message_with_gpg(secret, message, encoded=True):
    gpg = gnupg.GPG()
    if encoded:
        return base64.b64encode(
            str(
                gpg.encrypt(
                    message, symmetric="AES256", passphrase=secret, recipients=None
                )
            ).encode()
        ).decode()
    return str(
        gpg.encrypt(message, symmetric="AES256", passphrase=secret, recipients=None)
    )


def has_encrypted_header(message):
    return message.startswith(ENCRYPTED_HEADER_BEGIN) and message.endswith(
        ENCRYPTED_HEADER_END
    )


def decrypt_message_with_gpg(secret, message, encoded=True):
    gpg = gnupg.GPG()
    if not has_encrypted_header(message):
        return ""
    message = message[len(ENCRYPTED_HEADER_BEGIN) : -len(ENCRYPTED_HEADER_END)]
    if encoded:
        return str(gpg.decrypt(base64.b64decode(message).decode(), passphrase=secret))
    return str(gpg.decrypt(message, passphrase=secret))
