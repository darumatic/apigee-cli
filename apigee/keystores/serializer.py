import json


class KeystoresSerializer:
    def serialize_details(self, keystores, format, prefix=None):
        resp = keystores
        if format == 'text':
            return keystores.text
        keystores = keystores.json()
        if prefix:
            keystores = [keystore for keystore in keystores if keystore.startswith(prefix)]
        if format == 'json':
            return json.dumps(keystores)
        elif format == 'table':
            pass
        elif format == 'dict':
            return keystores
        return resp
