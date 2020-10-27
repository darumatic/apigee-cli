import json


class DevelopersSerializer:
    def serialize_details(self, developers, format, prefix=None):
        resp = developers
        if format == 'text':
            return developers.text
        developers = developers.json()
        if prefix:
            developers = [developer for developer in developers if developer.startswith(prefix)]
        if format == 'json':
            return json.dumps(developers)
        elif format == 'table':
            pass
        elif format == 'dict':
            return developers
        return resp
