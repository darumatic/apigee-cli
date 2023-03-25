import json


class AppsSerializer:
    def serialize_details(self, apps, format, prefix=None):
        resp = apps
        if format == "text":
            return apps.text
        apps = apps.json()
        if prefix:
            apps = [app for app in apps if app.startswith(prefix)]
        if format == "dict":
            return apps
        elif format == "json":
            return json.dumps(apps)
        return resp
