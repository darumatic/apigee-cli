import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.deployments.deployments import Deployments
from apigee.sharedflows.serializer import SharedflowsSerializer
from apigee.utils import merge_dict_values, apply_function_on_iterable, write_content_to_zip

GET_A_LIST_OF_SHARED_FLOWS_PATH = "{api_url}/v1/organizations/{org}/sharedflows"
IMPORT_A_SHARED_FLOW_PATH = "{api_url}/v1/organizations/{org}/sharedflows"
GET_A_SHARED_FLOW_PATH = "{api_url}/v1/organizations/{org}/sharedflows/{shared_flow_name}"
DEPLOY_A_SHARED_FLOW_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/sharedflows/{shared_flow_name}/revisions/{revision_number}/deployments"
UNDEPLOY_SHARED_FLOW_REVISIONS_IN_ENVIRONMENT_PATH = ""
UNDEPLOY_A_SHARED_FLOW_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/sharedflows/{shared_flow_name}/revisions/{revision_number}/deployments"
GET_DEPLOYMENT_ENVIRONMENTS_FOR_SHARED_FLOWS_PATH = "{api_url}/v1/organizations/{org}/sharedflows/{shared_flow_name}/revisions/{revision_number}/deployments"
DELETE_A_SHARED_FLOW_PATH = ""
DELETE_A_SHARED_FLOW_REVISION_PATH = "{api_url}/v1/organizations/{org}/sharedflows/{shared_flow_name}/revisions/{revision_number}"
GET_THE_SHARED_FLOW_ATTACHED_TO_A_FLOW_HOOK_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/flowhooks/{flow_hook}"
GET_SHARED_FLOW_DEPLOYMENTS_PATH = "{api_url}/v1/organizations/{org}/sharedflows/{shared_flow_name}/deployments"
GET_SHARED_FLOW_REVISIONS_PATH = "{api_url}/v1/organizations/{org}/sharedflows/{shared_flow_name}/revisions"
EXPORT_SHARED_FLOW_PATH = "{api_url}/v1/organizations/{org}/sharedflows/{shared_flow_name}/revisions/{revision_number}?format=bundle"


class Sharedflows:
    def __init__(self, auth, org_name):
        self.auth = auth
        self.org_name = org_name

    def delete_a_shared_flow_revision(self, shared_flow_name, revision_number):
        uri = DELETE_A_SHARED_FLOW_REVISION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            shared_flow_name=shared_flow_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        return self.delete_or_undeploy_a_shared_flow(uri, hdrs)

    def delete_undeployed_revisions(self, shared_flow_name, save_last=0, dry_run=False):
        details = SharedflowsSerializer.filter_deployment_details(
            Deployments(self.auth, self.org_name, shared_flow_name)
            .get_shared_flow_deployment_details()
            .json()
        )
        undeployed = SharedflowsSerializer.filter_undeployed_revisions(
            self.get_shared_flow_revisions(shared_flow_name).json(),
            SharedflowsSerializer.filter_deployed_revisions(details),
            save_last=save_last,
        )
        console.echo(f"Undeployed revisions to be deleted: {undeployed}")
        if dry_run:
            return undeployed

        def _func(revision):
            console.echo(f"Deleting revison {revision}")
            self.delete_a_shared_flow_revision(shared_flow_name, revision)

        return apply_function_on_iterable(undeployed, _func)

    def get_a_list_of_shared_flows(self, prefix=None):
        uri = GET_A_LIST_OF_SHARED_FLOWS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name
        )
        resp = self.fetch_shared_flow_revisions(uri)
        return SharedflowsSerializer.serialize_details(resp, "json", prefix=prefix)

    def import_a_shared_flow(self, shared_flow_file, shared_flow_name):
        uri = IMPORT_A_SHARED_FLOW_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            {"Accept": "application/json", "Content-Type": "multipart/form-data"},
        )
        params = {"action": "import", "name": shared_flow_name}
        with open(shared_flow_file, "rb") as f:
            resp = requests.post(
                uri, headers=hdrs, files={"file": ("sharedflow.zip", f)}, params=params
            )
        resp.raise_for_status()
        return resp

    def get_a_shared_flow(self, shared_flow_name):
        return self.retrieve_shared_flow_revisions(
            GET_A_SHARED_FLOW_PATH, shared_flow_name
        )

    def deploy_a_shared_flow(
        self,
        environment,
        shared_flow_name,
        revision_number,
        override=False,
        delay=0,
        shared_flow_file=None,
    ):
        do_deployments_exist = False
        try:
            if self.get_shared_flow_revisions(shared_flow_name):
                do_deployments_exist = True
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
        if shared_flow_file:
            revision_number = int(
                self.import_a_shared_flow(shared_flow_file, shared_flow_name).json()[
                    "revision"
                ]
            )
        uri = DEPLOY_A_SHARED_FLOW_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            shared_flow_name=shared_flow_name,
            revision_number=revision_number,
        )
        options_dict = {
            "override": "true" if override else "false",
            "delay": f"{delay}",
        }
        params = merge_dict_values(options_dict)
        hdrs = auth.set_authentication_headers(self.auth, {"Accept": "application/json"})
        console.echo(f"Deploying revision {revision_number}... ", line_ending="", should_flush=True)
        resp = requests.post(uri, headers=hdrs, params=params)
        resp.raise_for_status()
        console.echo("Done")
        if do_deployments_exist:
            # console.echo('Attempting undeployment... ')
            self.undeploy_shared_flow_revisions_in_environment(
                environment, shared_flow_name, except_revisions={revision_number}
            )
            # console.echo('Done.')
        return resp

    def undeploy_shared_flow_revisions_in_environment(
        self, environment, shared_flow_name, except_revisions=set()
    ):
        resp = self.get_shared_flow_deployments(shared_flow_name)
        for deployment in resp.json()["environment"]:
            if deployment["name"] == environment:
                for detail in deployment["revision"]:
                    revision_number = int(detail["name"])
                    if revision_number not in except_revisions:
                        console.echo(
                            f"Undeploying revision {revision_number}... ",
                            line_ending="",
                            should_flush=True,
                        )
                        self.undeploy_a_shared_flow(
                            environment, shared_flow_name, revision_number
                        )
                        console.echo("Done")
        return resp

    def undeploy_a_shared_flow(self, environment, shared_flow_name, revision_number):
        uri = UNDEPLOY_A_SHARED_FLOW_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            shared_flow_name=shared_flow_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_authentication_headers(self.auth, {"Accept": "application/json"})
        return self.delete_or_undeploy_a_shared_flow(uri, hdrs)

    def delete_or_undeploy_a_shared_flow(self, uri, hdrs):
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_deployment_environments_for_shared_flows(
        self, shared_flow_name, revision_number
    ):
        uri = GET_DEPLOYMENT_ENVIRONMENTS_FOR_SHARED_FLOWS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            shared_flow_name=shared_flow_name,
            revision_number=revision_number,
        )
        return self.fetch_shared_flow_revisions(uri)

    def get_the_shared_flow_attached_to_a_flow_hook(self, environment, flow_hook):
        uri = GET_THE_SHARED_FLOW_ATTACHED_TO_A_FLOW_HOOK_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            environment=environment,
            flow_hook=flow_hook,
        )
        return self.fetch_shared_flow_revisions(uri)

    def get_shared_flow_deployments(self, shared_flow_name):
        return self.retrieve_shared_flow_revisions(
            GET_SHARED_FLOW_DEPLOYMENTS_PATH, shared_flow_name
        )

    def get_shared_flow_revisions(self, shared_flow_name):
        return self.retrieve_shared_flow_revisions(
            GET_SHARED_FLOW_REVISIONS_PATH, shared_flow_name
        )

    def retrieve_shared_flow_revisions(self, endpoint_template, shared_flow_name):
        uri = endpoint_template.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            shared_flow_name=shared_flow_name,
        )
        return self.fetch_shared_flow_revisions(uri)

    def fetch_shared_flow_revisions(self, uri):
        hdrs = auth.set_authentication_headers(
            self.auth, {"Accept": "application/json"}
        )
        result = requests.get(uri, headers=hdrs)
        result.raise_for_status()
        return result

    def export_shared_flow(
        self, shared_flow_name, revision_number, output_file, write_to_filesystem=True
    ):
        uri = EXPORT_SHARED_FLOW_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            shared_flow_name=shared_flow_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_authentication_headers(self.auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        if write_to_filesystem and output_file:
            write_content_to_zip(output_file, resp.content)
        return resp
