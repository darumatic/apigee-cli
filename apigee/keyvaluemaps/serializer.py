import json


class KeyvaluemapsSerializer:
    def serialize_details(self, maps, format, prefix=None):
        resp = maps
        if format == "text":
            return maps.text
        maps = maps.json()
        if prefix:
            maps = [map for map in maps if map.startswith(prefix)]
        if format == "dict":
            return maps
        elif format == "json":
            return json.dumps(maps)
        return resp
