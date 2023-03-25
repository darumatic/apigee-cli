import json


class VirtualhostsSerializer:
    def serialize_details(self, virtualhosts, format, prefix=None):
        resp = virtualhosts
        if format == "text":
            return virtualhosts.text
        virtualhosts = virtualhosts.json()
        if prefix:
            virtualhosts = [
                virtualhost
                for virtualhost in virtualhosts
                if virtualhost.startswith(prefix)
            ]
        if format == "dict":
            return virtualhosts
        elif format == "json":
            return json.dumps(virtualhosts)
        return resp
