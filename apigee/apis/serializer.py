import json

from apigee.utils import remove_last_elements, apply_function_on_iterable


class ApisSerializer:
    @staticmethod
    def filter_deployed_revisions(revision_details):
        revisions = apply_function_on_iterable(revision_details, lambda d: d["revision"], state_op="extend")
        unique_revisions = set(revisions)
        return list(unique_revisions)

    @staticmethod
    def filter_deployment_details(deployment_details):
        return apply_function_on_iterable(
            deployment_details["environment"],
            lambda env: {
                "name": env["name"],
                "revision": [revision["name"] for revision in env["revision"]],
            },
        )

    @staticmethod
    def filter_undeployed_revisions(all_revisions, deployed_revisions, save_last=0):
        undeployed_revisions = [int(rev) for rev in all_revisions if rev not in set(deployed_revisions)]
        sorted_undeployed_revisions = sorted(undeployed_revisions)
        return remove_last_elements(sorted_undeployed_revisions, save_last)

    @staticmethod
    def serialize_details(apis, format, prefix=None):
        resp = apis
        if format == "text":
            return apis.text
        apis = apis.json()
        if prefix:
            apis = [api for api in apis if api.startswith(prefix)]
        if format == "dict":
            return apis
        elif format == "json":
            return json.dumps(apis)
        return resp
