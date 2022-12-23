import json


class KeyvaluemapsSerializer:
    def serialize_details(self, maps, format, prefix=None):
        resp = maps
        if format == "text":
            return maps.text
        maps = maps.json()
        if prefix:
            maps = [map for map in maps if map.startswith(prefix)]
        if format == "json":
            return json.dumps(maps)
        elif format == "table":
            pass
        elif format == "dict":
            return maps
        return resp
