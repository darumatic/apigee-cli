import requests

from apigee import APIGEE_ADMIN_API_URL, auth
from apigee.deployments.serializer import DeploymentsSerializer

GET_API_PROXY_DEPLOYMENT_DETAILS_PATH = "{api_url}/v1/organizations/{org}/apis/{api_name}/deployments"
GET_SHARED_FLOW_DEPLOYMENT_DETAILS_PATH = "{api_url}/v1/organizations/{org}/sharedflows/{shared_flow_name}/deployments"


class Deployments:
    def __init__(self, auth, org_name, name):
        self.auth = auth
        self.org_name = org_name
        self.name = name

    def get_api_proxy_deployment_details(
        self,
        formatted=False,
        format="text",
        showindex=False,
        tablefmt="plain",
        revision_name_only=False,
    ):
        uri = GET_API_PROXY_DEPLOYMENT_DETAILS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, api_name=self.name
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        if formatted:
            if revision_name_only:
                return DeploymentsSerializer().serialize_details(
                    resp, format, showindex=showindex, tablefmt=tablefmt
                )
            return DeploymentsSerializer().serialize_details(resp, "text")
        return resp

    def get_shared_flow_deployment_details(
        self,
        formatted=False,
        format="text",
        showindex=False,
        tablefmt="plain",
        revision_name_only=False,
    ):
        uri = GET_SHARED_FLOW_DEPLOYMENT_DETAILS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            shared_flow_name=self.name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        if formatted:
            if revision_name_only:
                return DeploymentsSerializer().serialize_details(
                    resp, format, showindex=showindex, tablefmt=tablefmt
                )
            return DeploymentsSerializer().serialize_details(resp, "text")
        return resp
