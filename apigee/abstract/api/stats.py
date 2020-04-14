#!/usr/bin/env python
"""https://apidocs.apigee.com/api/stats"""

import json
from abc import ABC, abstractmethod


class IStats:
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
    def get_license_utilization(self, time_range, environments=["test", "prod"], tzo=None, api_calls_per_year=10000000000):
        pass


class StatsSerializer:
    def serialize_details(self, stats, format, prefix=None):
        resp = stats
        if format == "text":
            return stats.text
        stats = stats.json()
        if prefix:
            stats = [stat for stat in stats if stat.startswith(prefix)]
        if format == "json":
            return json.dumps(stats)
        elif format == "table":
            pass
        # else:
        #     raise ValueError(format)
        return resp
