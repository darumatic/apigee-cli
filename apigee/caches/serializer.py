import json


class CachesSerializer:
    def serialize_details(self, caches, format, prefix=None):
        resp = caches
        if format == "text":
            return caches.text
        caches = caches.json()
        if prefix:
            caches = [cache for cache in caches if cache.startswith(prefix)]
        if format == "dict":
            return caches
        elif format == "json":
            return json.dumps(caches)
        return resp
