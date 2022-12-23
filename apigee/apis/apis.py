from pathlib import Path

import requests

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.apis.serializer import ApisSerializer
from apigee.deployments.deployments import Deployments
from apigee.utils import run_func_on_iterable, write_zip

DELETE_API_PROXY_REVISION_PATH = (
    "{api_url}/v1/organizations/{org}/apis/{api_name}/revisions/{revision_number}"
)
DEPLOY_API_PROXY_REVISION_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/apis/{api_name}/revisions/{revision_number}/deployments?delay={delay}"
EXPORT_API_PROXY_PATH = "{api_url}/v1/organizations/{org}/apis/{api_name}/revisions/{revision_number}?format=bundle"
GET_API_PROXY_PATH = "{api_url}/v1/organizations/{org}/apis/{api_name}"
LIST_API_PROXIES_PATH = "{api_url}/v1/organizations/{org}/apis"
LIST_API_PROXY_REVISIONS_PATH = (
    "{api_url}/v1/organizations/{org}/apis/{api_name}/revisions"
)
UNDEPLOY_API_PROXY_REVISION_PATH = "{api_url}/v1/organizations/{org}/environments/{environment}/apis/{api_name}/revisions/{revision_number}/deployments"
FORCE_UNDEPLOY_API_PROXY_REVISION_PATH = "{api_url}/v1/organizations/{org}/apis/{api_name}/revisions/{revision_number}/deployments?action=undeploy&env={environment}&force=true"


class Apis:
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

    def delete_api_proxy_revision(self, api_name, revision_number):
        uri = DELETE_API_PROXY_REVISION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            api_name=api_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def deploy_api_proxy_revision(
        self, api_name, environment, revision_number, delay=0, override=False
    ):
        uri = DEPLOY_API_PROXY_REVISION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            api_name=api_name,
            revision_number=revision_number,
            delay=delay,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        resp = requests.post(
            uri, headers=hdrs, data={"override": "true" if override else "false"}
        )
        resp.raise_for_status()
        return resp

    def delete_undeployed_revisions(self, api_name, save_last=0, dry_run=False):
        details = ApisSerializer.filter_deployment_details(
            Deployments(self._auth, self._org_name, api_name)
            .get_api_proxy_deployment_details()
            .json()
        )
        undeployed = ApisSerializer.filter_undeployed_revisions(
            self.list_api_proxy_revisions(api_name).json(),
            ApisSerializer.filter_deployed_revisions(details),
            save_last=save_last,
        )
        console.echo(f"Undeployed revisions to be deleted: {undeployed}")
        if dry_run:
            return undeployed

        def _func(revision):
            console.echo(f"Deleting revison {revision}")
            self.delete_api_proxy_revision(api_name, revision)

        return run_func_on_iterable(undeployed, _func)

    def export_api_proxy(
        self, api_name, revision_number, fs_write=True, output_file=None
    ):
        uri = EXPORT_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            api_name=api_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        if fs_write:
            write_zip(output_file, resp.content)
        return resp

    def get_api_proxy(self, api_name):
        uri = GET_API_PROXY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, api_name=api_name
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_api_proxies(self, prefix=None, format="json"):
        uri = LIST_API_PROXIES_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return ApisSerializer.serialize_details(resp, format, prefix=prefix)

    def list_api_proxy_revisions(self, api_name):
        uri = LIST_API_PROXY_REVISIONS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, api_name=api_name
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def undeploy_api_proxy_revision(self, api_name, environment, revision_number):
        uri = UNDEPLOY_API_PROXY_REVISION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            environment=environment,
            api_name=api_name,
            revision_number=revision_number,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def force_undeploy_api_proxy_revision(self, api_name, environment, revision_number):
        uri = FORCE_UNDEPLOY_API_PROXY_REVISION_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            api_name=api_name,
            revision_number=revision_number,
            environment=environment,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp
