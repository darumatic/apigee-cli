import json

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.sharedflows.serializer import SharedflowsSerializer
from apigee.utils import add_to_dict_if_exists

GET_A_LIST_OF_SHARED_FLOWS_PATH = '{api_url}/v1/organizations/{org}/sharedflows'
IMPORT_A_SHARED_FLOW_PATH = '{api_url}/v1/organizations/{org}/sharedflows'
# EXPORT_A_SHARED_FLOW_PATH = ''
GET_A_SHARED_FLOW_PATH = '{api_url}/v1/organizations/{org}/sharedflows/{shared_flow_name}'
DEPLOY_A_SHARED_FLOW_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/sharedflows/{shared_flow_name}/revisions/{revision_number}/deployments'
UNDEPLOY_SHARED_FLOW_REVISIONS_IN_ENVIRONMENT_PATH = ''
UNDEPLOY_A_SHARED_FLOW_PATH = '{api_url}/v1/organizations/{org}/environments/{environment}/sharedflows/{shared_flow_name}/revisions/{revision_number}/deployments'
GET_DEPLOYMENT_ENVIRONMENTS_FOR_SHARED_FLOWS_PATH = '{api_url}/v1/organizations/{org}/sharedflows/{shared_flow_name}/revisions/{revision_number}/deployments'
DELETE_A_SHARED_FLOW_PATH = ''
# ATTACH_A_SHARED_FLOW_TO_A_FLOW_HOOK_PATH = ''
# DETACHES_A_SHARED_FLOW_FROM_A_FLOW_HOOK_PATH = ''
GET_THE_SHARED_FLOW_ATTACHED_TO_A_FLOW_HOOK_PATH = (
    '{api_url}/v1/organizations/{org}/environments/{environment}/flowhooks/{flow_hook}'
)
GET_SHARED_FLOW_DEPLOYMENTS_PATH = (
    '{api_url}/v1/organizations/{org}/sharedflows/{shared_flow_name}/deployments'
)
GET_SHARED_FLOW_REVISIONS_PATH = (
    '{api_url}/v1/organizations/{org}/sharedflows/{shared_flow_name}/revisions'
)


class Sharedflows:
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

    def get_a_list_of_shared_flows(self, prefix=None):
        uri = GET_A_LIST_OF_SHARED_FLOWS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name
        )
        hdrs = auth.set_header(self._auth, {'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return SharedflowsSerializer().serialize_details(resp, 'json', prefix=prefix)

    def import_a_shared_flow(self, shared_flow_file, shared_flow_name):
        uri = IMPORT_A_SHARED_FLOW_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name)
        hdrs = auth.set_header(
            self._auth, {'Accept': 'application/json', 'Content-Type': 'multipart/form-data'}
        )
        params = {'action': 'import', 'name': shared_flow_name}
        with open(shared_flow_file, 'rb') as f:
            resp = requests.post(
                uri, headers=hdrs, files={'file': ('sharedflow.zip', f)}, params=params
            )
        resp.raise_for_status()
        return resp

    # def export_a_shared_flow(self, shared_flow_name, revision_number):
    #     pass

    def get_a_shared_flow(self, shared_flow_name):
        uri = GET_A_SHARED_FLOW_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, shared_flow_name=shared_flow_name
        )
        hdrs = auth.set_header(self._auth, {'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

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
                self.import_a_shared_flow(shared_flow_file, shared_flow_name).json()['revision']
            )
        uri = DEPLOY_A_SHARED_FLOW_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            shared_flow_name=shared_flow_name,
            revision_number=revision_number,
        )
        options_dict = {'override': 'true' if override else 'false', 'delay': f'{delay}'}
        params = add_to_dict_if_exists(options_dict)
        hdrs = auth.set_header(self._auth, {'Accept': 'application/json'})
        console.echo(f'Deploying revision {revision_number}... ', end='', flush=True)
        resp = requests.post(uri, headers=hdrs, params=params)
        resp.raise_for_status()
        console.echo('Done')
        if do_deployments_exist:
            console.echo('Attempting undeployment... ')
            self.undeploy_shared_flow_revisions_in_environment(
                environment, shared_flow_name, except_revisions={revision_number}
            )
            console.echo('Done.')
        return resp

    def undeploy_shared_flow_revisions_in_environment(
        self, environment, shared_flow_name, except_revisions=set()
    ):
        resp = self.get_shared_flow_deployments(shared_flow_name)
        for deployment in resp.json()['environment']:
            if deployment['name'] == environment:
                for detail in deployment['revision']:
                    revision_number = int(detail['name'])
                    if revision_number not in except_revisions:
                        console.echo(
                            f'Undeploying revision {revision_number}... ', end='', flush=True
                        )
                        self.undeploy_a_shared_flow(environment, shared_flow_name, revision_number)
                        console.echo('Done')
        return resp

    def undeploy_a_shared_flow(self, environment, shared_flow_name, revision_number):
        uri = UNDEPLOY_A_SHARED_FLOW_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            shared_flow_name=shared_flow_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_header(self._auth, {'Accept': 'application/json'})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_deployment_environments_for_shared_flows(self, shared_flow_name, revision_number):
        uri = GET_DEPLOYMENT_ENVIRONMENTS_FOR_SHARED_FLOWS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            shared_flow_name=shared_flow_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_header(self._auth, {'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_a_shared_flow(self, shared_flow_name):
        pass

    # def attach_a_shared_flow_to_a_flow_hook(self, environment, flow_hook, request_body):
    #     pass
    #
    # def detaches_a_shared_flow_from_a_flow_hook(self, environment, flow_hook):
    #     pass

    def get_the_shared_flow_attached_to_a_flow_hook(self, environment, flow_hook):
        uri = GET_THE_SHARED_FLOW_ATTACHED_TO_A_FLOW_HOOK_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            flow_hook=flow_hook,
        )
        hdrs = auth.set_header(self._auth, {'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_shared_flow_deployments(self, shared_flow_name):
        uri = GET_SHARED_FLOW_DEPLOYMENTS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, shared_flow_name=shared_flow_name
        )
        hdrs = auth.set_header(self._auth, {'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_shared_flow_revisions(self, shared_flow_name):
        uri = GET_SHARED_FLOW_REVISIONS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, shared_flow_name=shared_flow_name
        )
        hdrs = auth.set_header(self._auth, {'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp
