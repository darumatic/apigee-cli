import json


class ReferencesSerializer:
    def serialize_details(self, references, format, prefix=None):
        resp = references
        if format == 'text':
            return references.text
        references = references.json()
        if prefix:
            references = [reference for reference in references if reference.startswith(prefix)]
        if format == 'json':
            return json.dumps(references)
        elif format == 'table':
            pass
        elif format == 'dict':
            return references
        return resp
