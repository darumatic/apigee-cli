import json


class CachesSerializer:
    def serialize_details(self, caches, format, prefix=None):
        resp = caches
        if format == "text":
            return caches.text
        caches = caches.json()
        if prefix:
            caches = [cache for cache in caches if cache.startswith(prefix)]
        if format == "json":
            return json.dumps(caches)
        elif format == "table":
            pass
        elif format == "dict":
            return caches
        return resp
