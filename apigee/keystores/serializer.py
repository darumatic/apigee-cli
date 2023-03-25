import json


class KeystoresSerializer:
    def serialize_details(self, keystores, format, prefix=None):
        resp = keystores
        if format == "text":
            return keystores.text
        keystores = keystores.json()
        if prefix:
            keystores = [
                keystore for keystore in keystores if keystore.startswith(prefix)
            ]
        if format == "dict":
            return keystores
        elif format == "json":
            return json.dumps(keystores)
        return resp
