import json

from apigee.utils import remove_last_items_from_list, run_func_on_iterable


class SharedflowsSerializer:
    @staticmethod
    def filter_deployed_revisions(details):
        return list(
            set(
                run_func_on_iterable(
                    details, lambda d: d["revision"], state_op="extend"
                )
            )
        )

    @staticmethod
    def filter_deployment_details(details):
        return run_func_on_iterable(
            details["environment"],
            lambda d: {
                "name": d["name"],
                "revision": [revision["name"] for revision in d["revision"]],
            },
        )

    @staticmethod
    def filter_undeployed_revisions(revisions, deployed, save_last=0):
        undeployed = [int(rev) for rev in revisions if rev not in deployed]
        return remove_last_items_from_list(sorted(undeployed), save_last)

    @staticmethod
    def serialize_details(sharedflows, format, prefix=None):
        resp = sharedflows
        if format == "text":
            return sharedflows.text
        sharedflows = sharedflows.json()
        if prefix:
            sharedflows = [
                sharedflow
                for sharedflow in sharedflows
                if sharedflow.startswith(prefix)
            ]
        if format == "json":
            return json.dumps(sharedflows)
        elif format == "table":
            pass
        return resp
