#!/usr/bin/env python
"""https://apidocs.apigee.com/api/debug-sessions"""

from abc import ABC, abstractmethod


class IDebugsessions:
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
    def create_a_debug_session(
        self,
        environment,
        api_name,
        revision_number,
        session_name,
        timeout=600,
        filter="",
    ):
        pass

    @abstractmethod
    def delete_debug_session(
        self, environment, api_name, revision_number, session_name
    ):
        pass

    @abstractmethod
    def list_debug_sessions(self, environment, api_name, revision_number):
        pass

    @abstractmethod
    def get_debug_session_transaction_IDs(
        self, environment, api_name, revision_number, session_name
    ):
        pass

    @abstractmethod
    def get_debug_session_transaction_data(
        self, environment, api_name, revision_number, session_name, transaction_id
    ):
        pass


class DebugsessionsSerializer:
    def serialize_details(self, sessions, format, prefix=None):
        resp = sessions
        if format == "text":
            return sessions.text
        sessions = sessions.json()
        if prefix:
            sessions = [api for api in sessions if api.startswith(prefix)]
        if format == "json":
            return json.dumps(sessions)
        elif format == "table":
            pass
        # else:
        #     raise ValueError(format)
        return resp
