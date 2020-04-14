#!/usr/bin/env python
"""https://apidocs.apigee.com/api/stats"""

import json
import requests
import urllib.parse

from tabulate import tabulate

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.stats import IStats, StatsSerializer
from apigee.util import authorization, console


class Stats(IStats):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_license_utilization(
        self, time_range, environments=["test", "prod"], tzo=None, api_calls_per_year=10000000000
    ):
        metrics = {}
        for env in environments:
            uri = f"{APIGEE_ADMIN_API_URL}/v1/o/{self._org_name}/environments/{env}/stats?select=sum(message_count)&timeRange={urllib.parse.quote(time_range)}"
            params = {}
            if tzo:
                params["tzo"] = tzo
            hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
            resp = requests.get(uri, headers=hdrs, params=params)
            resp.raise_for_status()
            for detail in resp.json()["environments"]:
                if detail["name"] == env:
                    for metric in detail["metrics"]:
                        if metric["name"] == "sum(message_count)":
                            metrics[env] = int(float(metric["values"][0]))
        console.log()
        console.log(f"Apigee license per year: {api_calls_per_year:,} API calls")
        # console.log(
        #     f'Current license utilization per environment in "{self._org_name}" org: '
        # )
        console.log()
        table = [[k, f"{v:,}"] for k, v in metrics.items()]
        headers = ["environment", "API calls"]
        t = tabulate(table, headers)
        # t = tabulate(table, headers, showindex=showindex, tablefmt=tablefmt)
        console.log(t)
        console.log()
        total = sum(metrics.values())
        console.log(f"Total API calls for specified time range ({time_range}): {total:,}")
        utilization = total*100 / api_calls_per_year
        console.log(f"Utilization % for specified time range ({time_range}): {utilization}%")
        console.log()
        return t
