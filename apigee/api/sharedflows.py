#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/shared-flows-and-flow-hooks-management-api"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.sharedflows import ISharedflows, SharedflowsSerializer
from apigee.util import authorization, console


class Sharedflows(ISharedflows):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_a_list_of_shared_flows(self, prefix=None):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/sharedflows"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return SharedflowsSerializer().serialize_details(resp, "json", prefix=prefix)

    def import_a_shared_flow(self, shared_flow_file, shared_flow_name):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/sharedflows?action=import&name={shared_flow_name}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "multipart/form-data"},
            self._auth,
        )
        with open(shared_flow_file, "rb") as f:
            resp = requests.post(
                uri, headers=hdrs, files={"file": ("sharedflow.zip", f)}
            )
        resp.raise_for_status()
        return resp

    # def export_a_shared_flow(self, shared_flow_name, revision_number):
    #     pass

    def get_a_shared_flow(self, shared_flow_name):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/sharedflows/{shared_flow_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def deploy_a_shared_flow(
        self,
        environment,
        shared_flow_name,
        revision_number,
        override=False,
        delay=0,
        shared_flow_file=None,
    ):
        # we need to undeploy existing deployed revisions in the target environment first,
        # otherwise each revision will remain deployed (will not undeploy with each new revision)
        self.undeploy_shared_flow_revisions_in_environment(
            environment, shared_flow_name
        )
        if shared_flow_file:
            revision_number = int(
                self.import_a_shared_flow(shared_flow_file, shared_flow_name).json()[
                    "revision"
                ]
            )
        # the `override` query parameter does not seem to work on Apigee Edge,
        # therefore we need to run undeploy_shared_flow_revisions_in_environment() first (as above)
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/sharedflows/{shared_flow_name}/revisions/{revision_number}/deployments?override={'true' if override else 'false'}&delay={delay}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth,)
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def undeploy_shared_flow_revisions_in_environment(
        self, environment, shared_flow_name
    ):
        resp = self.get_shared_flow_deployments(shared_flow_name)
        for deployment in resp.json()["environment"]:
            if deployment["name"] == environment:
                for detail in deployment["revision"]:
                    revision_number = int(detail["name"])
                    self.undeploy_a_shared_flow(
                        environment, shared_flow_name, revision_number
                    )
        return resp

    def undeploy_a_shared_flow(self, environment, shared_flow_name, revision_number):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/sharedflows/{shared_flow_name}/revisions/{revision_number}/deployments"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_deployment_environments_for_shared_flows(
        self, shared_flow_name, revision_number
    ):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/sharedflows/{shared_flow_name}/revisions/{revision_number}/deployments"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_a_shared_flow(self, shared_flow_name):
        pass

    # def attach_a_shared_flow_to_a_flow_hook(self, environment, flow_hook, request_body):
    #     pass
    #
    # def detaches_a_shared_flow_from_a_flow_hook(self, environment, flow_hook):
    #     pass

    def get_the_shared_flow_attached_to_a_flow_hook(self, environment, flow_hook):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/flowhooks/{flow_hook}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_shared_flow_deployments(self, shared_flow_name):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/sharedflows/{shared_flow_name}/deployments"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_shared_flow_revisions(self, shared_flow_name):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/sharedflows/{shared_flow_name}/revisions"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp
