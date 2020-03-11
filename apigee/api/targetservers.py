#!/usr/bin/env python
"""Source: https://apidocs.apigee.com/api/api_resources/51-targetservers

TargetServers are used to decouple TargetEndpoint HTTPTargetConnections from
concrete URLs for backend services.

To do so, an HTTPConnection can be configured to use a LoadBalancer that lists
one or more 'named' TargetSevers.
Using TargetServers, you can create an HTTPTargetConnection that calls a
different backend server based on the environment where the API proxy is
deployed.
"""

import json
import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.targetservers import ITargetservers, TargetserversSerializer
from apigee.util import authorization, console


class Targetservers(ITargetservers):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_a_targetserver(self, environment, request_body):
        """Create a TargetServer in the specified environment.

        Args:
            environment (str): Apigee environment.
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/targetservers"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_a_targetserver(self, environment):
        """Delete a TargetServer configuration from an environment.

        Args:
            environment (str): Apigee environment.

        Returns:
            requests.Response(): Information about the deleted TargetServer.
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/targetservers/{self._targetserver_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_targetservers_in_an_environment(self, environment, prefix=None):
        """List all TargetServers in an environment.

        Args:
            environment (str): Apigee environment.
            prefix (str, optional): Filter results by a prefix string.
                Defaults to None.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/targetservers"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return TargetserversSerializer().serialize_details(resp, "json", prefix=prefix)

    def get_targetserver(self, environment):
        """Returns a TargetServer definition.

        Args:
            environment (str): Apigee environment.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/targetservers/{self._targetserver_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def update_a_targetserver(self, environment, request_body):
        """Modifies an existing TargetServer.

        Note: In the request body when Content-Type is set to application/json,
        use the element sSLInfo in the request body, not SSLInfo (note the
        case).
        You must use the case sSLInfo exactly.
        Using SSLInfo will cause an error when Content-Type is set to
        application/json.
        The case does not matter if Content-Type is application/xml.

        Args:
            environment (str): Apigee environment.
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/environments/{environment}/targetservers/{self._targetserver_name}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def push_targetserver(self, environment, file):
        """Push TargetSever file to Apigee

        This will create a TargetSever if it does not exist and update if it
        does.

        Args:
            environment (str): Apigee environment.
            file (str): The file path.

        Returns:
            None

        Raises:
            HTTPError: If response status code is not successful or 404.
        """
        with open(file) as f:
            body = f.read()
        targetserver = json.loads(body)
        self._targetserver_name = targetserver["name"]
        try:
            self.get_targetserver(environment)
            console.log("Updating", self._targetserver_name)
            console.log(self.update_a_targetserver(environment, body).text)
        except HTTPError as e:
            if e.response.status_code not in [404]:
                raise e
            console.log("Creating", self._targetserver_name)
            console.log(self.create_a_targetserver(environment, body).text)
