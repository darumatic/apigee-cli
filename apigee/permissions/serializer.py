import json

from tabulate import tabulate


class PermissionsSerializer:
    def serialize_details(
        self, permission_details, format, showindex=False, tablefmt="plain"
    ):
        if format == "text":
            return permission_details.text
        elif format == "json":
            return permission_details.json()
        elif format == "table":
            table = [
                [res["organization"], res["path"], res["permissions"]]
                for res in permission_details.json()["resourcePermission"]
            ]
            headers = []
            if showindex == "always" or showindex is True:
                headers = ["id", "organization", "path", "permissions"]
            elif showindex == "never" or showindex is False:
                headers = ["organization", "path", "permissions"]
            return tabulate(table, headers, showindex=showindex, tablefmt=tablefmt)
        return permission_details
