import json


class ApisSerializer:
    def serialize_details(self, apis, format, prefix=None):
        resp = apis
        if format == 'text':
            return apis.text
        apis = apis.json()
        if prefix:
            apis = [api for api in apis if api.startswith(prefix)]
        if format == 'json':
            return json.dumps(apis)
        elif format == 'table':
            pass
        elif format == 'dict':
            return apis
        return resp
