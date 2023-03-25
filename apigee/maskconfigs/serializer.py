import json


class MaskconfigsSerializer:
    def serialize_details(self, maskconfigs, format, prefix=None):
        resp = maskconfigs
        if format == "text":
            return maskconfigs.text
        maskconfigs = maskconfigs.json()
        if prefix:
            maskconfigs = [
                maskconfig
                for maskconfig in maskconfigs
                if maskconfig.startswith(prefix)
            ]
        return json.dumps(maskconfigs) if format == "json" else resp
