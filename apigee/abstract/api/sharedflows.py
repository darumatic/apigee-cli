#!/usr/bin/env python
"""https://apidocs.apigee.com/api-reference/content/shared-flows-and-flow-hooks-management-api"""

import json
from abc import ABC, abstractmethod


class ISharedflows:
    def __init__(self, auth, org_name):
        self._auth = auth
        self._org_name = org_name

    def __call__(self):
        pass

    @property
    def auth(self):
        return self._auth

    @auth.setter
    def auth(self, value):
        self._auth = value

    @property
    def org_name(self):
        return self._org_name

    @org_name.setter
    def org_name(self, value):
        self._org_name = value

    @abstractmethod
    def get_a_list_of_shared_flows(self, prefix=None):
        pass

    @abstractmethod
    def import_a_shared_flow(self, shared_flow_file, shared_flow_name):
        pass

    @abstractmethod
    def export_a_shared_flow(self, shared_flow_name, revision_number):
        pass

    @abstractmethod
    def get_a_shared_flow(self, shared_flow_name):
        pass

    @abstractmethod
    def deploy_a_shared_flow(
        self,
        environment,
        shared_flow_name,
        revision_number,
        override=False,
        delay=0,
        shared_flow_file=None,
    ):
        pass

    @abstractmethod
    def undeploy_a_shared_flow(self, environment, shared_flow_name, revision_number):
        pass

    @abstractmethod
    def get_deployment_environments_for_shared_flows(
        self, shared_flow_name, revision_number
    ):
        pass

    @abstractmethod
    def delete_a_shared_flow(self, shared_flow_name):
        pass

    @abstractmethod
    def attach_a_shared_flow_to_a_flow_hook(self, environment, flow_hook, request_body):
        pass

    @abstractmethod
    def detaches_a_shared_flow_from_a_flow_hook(self, environment, flow_hook):
        pass

    @abstractmethod
    def get_the_shared_flow_attached_to_a_flow_hook(self, environment, flow_hook):
        pass

    @abstractmethod
    def get_shared_flow_deployments(self, shared_flow_name):
        pass

    @abstractmethod
    def get_shared_flow_revisions(self, shared_flow_name):
        pass


class SharedflowsSerializer:
    def serialize_details(self, sharedflows, format, prefix=None):
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
        # else:
        #     raise ValueError(format)
        return resp
