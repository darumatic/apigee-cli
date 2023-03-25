import json


class TargetserversSerializer:
    def serialize_details(self, targetservers, format, prefix=None):
        resp = targetservers
        if format == "text":
            return targetservers.text
        targetservers = targetservers.json()
        if prefix:
            targetservers = [
                targetserver
                for targetserver in targetservers
                if targetserver.startswith(prefix)
            ]
        if format == "dict":
            return targetservers
        elif format == "json":
            return json.dumps(targetservers)
        return resp
