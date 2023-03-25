import json


class ReferencesSerializer:
    def serialize_details(self, references, format, prefix=None):
        resp = references
        if format == "text":
            return references.text
        references = references.json()
        if prefix:
            references = [
                reference for reference in references if reference.startswith(prefix)
            ]
        if format == "dict":
            return references
        elif format == "json":
            return json.dumps(references)
        return resp
