import json

from apigee.utils import remove_last_items_from_list, run_func_on_iterable


class ApisSerializer:
    def filter_deployed_revisions(self, details):
        return list(set(run_func_on_iterable(details, lambda d: d['revision'], state_op='extend')))

    def filter_deployment_details(self, details):
        return run_func_on_iterable(
            details['environment'],
            lambda d: {
                'name': d['name'],
                'revision': [revision['name'] for revision in d['revision']],
            },
        )

    def filter_undeployed_revisions(self, revisions, deployed, save_last=0):
        return remove_last_items_from_list(
            sorted([int(rev) for rev in revisions if rev not in deployed]), save_last
        )

    def serialize_details(self, apis, format, prefix=None):
        resp = apis
        if format == 'text':
            return apis.text
        apis = apis.json()
        if prefix:
            apis = [api for api in apis if api.startswith(prefix)]
        if format == 'json':
            return json.dumps(apis)
        elif format == 'table':
            pass
        elif format == 'dict':
            return apis
        return resp
