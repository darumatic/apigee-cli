#!/usr/bin/env python
"""Source: https://apidocs.apigee.com/api/deployments

API Platform Base Path: https://api.enterprise.apigee.com/v1/o/{org_name}

API Resource Path: /apis/{api_name}/deployments

API proxies that are actively deployed in environments on Apigee Edge.
"""

import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.deployments import IDeployments, DeploymentsSerializer
from apigee.util import authorization


class Deployments(IDeployments):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_api_proxy_deployment_details(
        self,
        formatted=False,
        format="text",
        showindex=False,
        tablefmt="plain",
        revision_name_only=False,
    ):
        """Gets details for a specific API proxy deployed in a given environment

        Args:
            formatted (bool, optional): If True, format ``requests.Response()``.
                Defaults to False.
            format (str, optional): Specify how to format response.
                Defaults to 'text'.
            showindex (bool, optional): If True, show table index.
                Defaults to False.
            tablefmt (str, optional): Specify table format. Defaults to 'plain'.
            revision_name_only (bool, optional): If True, truncate response
                information.
                Defaults to False.

        Returns:
            requests.Response(): Response if ``formatted`` is False,
            else return a ``formatted`` value.
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/apis/{self._api_name}/deployments"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        if formatted:
            if revision_name_only:
                # return DeploymentsSerializer().serialize_details(resp, 'table', max_colwidth=args.max_colwidth)
                return DeploymentsSerializer().serialize_details(
                    resp, format, showindex=showindex, tablefmt=tablefmt
                )
            return DeploymentsSerializer().serialize_details(resp, "text")
        return resp
