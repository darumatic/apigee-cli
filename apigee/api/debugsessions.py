#!/usr/bin/env python
"""Source: https://apidocs.apigee.com/api/debug-sessions

API Platform Base Path: https://api.enterprise.apigee.com/v1/o/{org_name}

API Resource Path: /debugsessions

A session configured in Apigee Edge to record specified messages and associated
pipeline processing metadata for debugging purposes
"""

import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.debugsessions import IDebugsessions
from apigee.util import authorization


class Debugsessions(IDebugsessions):
    def __init__(self, auth, org_name):
        self._auth = auth
        self._org_name = org_name

    def create_a_debug_session(
        self,
        environment,
        api_name,
        revision_number,
        session_name,
        timeout=600,
        filter="",
    ):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/apis/{api_name}/revisions/{revision_number}/debugsessions?session={session_name}&timeout={timeout}"
        hdrs = authorization.set_header(
            {
                "Accept": "application/json",
                "Content-Type": "application/x-www-url-form-encoded",
            },
            self._auth,
        )
        if filter:
            uri += f"&{filter}"
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_debug_session(
        self, environment, api_name, revision_number, session_name
    ):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/apis/{api_name}/revisions/{revision_number}/debugsessions/{session_name}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_debug_sessions(self, environment, api_name, revision_number):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/apis/{api_name}/revisions/{revision_number}/debugsessions"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_debug_session_transaction_IDs(
        self, environment, api_name, revision_number, session_name
    ):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/apis/{api_name}/revisions/{revision_number}/debugsessions/{session_name}/data"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_debug_session_transaction_data(
        self, environment, api_name, revision_number, session_name, transaction_id
    ):
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/apis/{api_name}/revisions/{revision_number}/debugsessions/{session_name}/data/{transaction_id}"
        hdrs = authorization.set_header({"Accept": "application/xml"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp
