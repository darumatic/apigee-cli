import requests
from apigee import APIGEE_ADMIN_API_URL, auth
from apigee.virtualhosts.serializer import VirtualhostsSerializer

CREATE_A_VIRTUAL_HOST_FOR_AN_ENVIRONMENT_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/virtualhosts"
DELETE_A_VIRTUAL_HOST_FROM_AN_ENVIRONMENT_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/virtualhosts/{virtualhost_name}"
GET_A_VIRTUAL_HOST_FOR_AN_ENVIRONMENT_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/virtualhosts/{virtualhost_name}"
LIST_VIRTUAL_HOSTS_FOR_AN_ENVIRONMENT_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/virtualhosts"
UPDATE_VIRTUAL_HOST_FOR_AN_ENVIRONMENT_PATH = "{api_url}/v1/o/{org_name}/environments/{environment}/virtualhosts/{virtualhost_name}"


class Virtualhosts:
    def __init__(self, auth, org_name, virtualhost_name):
        self.auth = auth
        self.org_name = org_name
        self.virtualhost_name = virtualhost_name

    def get_a_virtual_host_for_an_environment(self, environment):
        uri = self._get_virtual_host_uri(environment)
        return self._get_virtual_hosts_for_environment(uri)

    def list_virtual_hosts_for_an_environment(self, environment, prefix=None, format="json"):
        uri = self._get_virtual_hosts_uri(environment)
        resp = self._get_virtual_hosts_for_environment(uri)
        return VirtualhostsSerializer().serialize_details(resp, format, prefix=prefix)

    def _get_virtual_host_uri(self, environment):
        return GET_A_VIRTUAL_HOST_FOR_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
            virtualhost_name=self.virtualhost_name,
        )

    def _get_virtual_hosts_uri(self, environment):
        return LIST_VIRTUAL_HOSTS_FOR_AN_ENVIRONMENT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org_name=self.org_name,
            environment=environment,
        )

    def _get_virtual_hosts_for_environment(self, uri):
        headers = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        result = requests.get(uri, headers=headers)
        result.raise_for_status()
        return result
