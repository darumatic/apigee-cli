import json


class SharedflowsSerializer:
    def serialize_details(self, sharedflows, format, prefix=None):
        resp = sharedflows
        if format == 'text':
            return sharedflows.text
        sharedflows = sharedflows.json()
        if prefix:
            sharedflows = [
                sharedflow for sharedflow in sharedflows if sharedflow.startswith(prefix)
            ]
        if format == 'json':
            return json.dumps(sharedflows)
        elif format == 'table':
            pass
        return resp
