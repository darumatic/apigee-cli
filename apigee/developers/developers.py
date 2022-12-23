import json
import random
import string

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth
from apigee.developers.serializer import DevelopersSerializer

CREATE_DEVELOPER_PATH = "{api_url}/v1/organizations/{org}/developers"
DELETE_DEVELOPER_PATH = "{api_url}/v1/organizations/{org}/developers/{developer_email}"
GET_DEVELOPER_PATH = "{api_url}/v1/organizations/{org}/developers/{developer_email}"
GET_DEVELOPER_BY_APP_PATH = "{api_url}/v1/organizations/{org}/developers?app={app_name}"
LIST_DEVELOPERS_PATH = "{api_url}/v1/organizations/{org}/developers?expand={expand}&count={count}&startKey={startkey}"
SET_DEVELOPER_STATUS_PATH = (
    "{api_url}/v1/organizations/{org}/developers/{developer_email}?action={action}"
)
UPDATE_DEVELOPER_PATH = "{api_url}/v1/organizations/{org}/developers/{developer_email}"
GET_DEVELOPER_ATTRIBUTE_PATH = "{api_url}/v1/organizations/{org}/developers/{developer_email}/attributes/{attribute_name}"
UPDATE_A_DEVELOPER_ATTRIBUTE_PATH = "{api_url}/v1/organizations/{org}/developers/{developer_email}/attributes/{attribute_name}"
DELETE_DEVELOPER_ATTRIBUTE_PATH = "{api_url}/v1/organizations/{org}/developers/{developer_email}/attributes/{attribute_name}"
GET_ALL_DEVELOPER_ATTRIBUTES_PATH = (
    "{api_url}/v1/organizations/{org}/developers/{developer_email}/attributes"
)
UPDATE_ALL_DEVELOPER_ATTRIBUTES_PATH = (
    "{api_url}/v1/organizations/{org}/developers/{developer_email}/attributes"
)


class Developers:
    def __init__(self, auth, org_name, developer_email):
        self._auth = auth
        self._org_name = org_name
        self._developer_email = developer_email

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

    @property
    def developer_email(self):
        return self._developer_email

    @developer_email.setter
    def developer_email(self, value):
        self._developer_email = value

    def __call__(self):
        pass

    def create_developer(
        self, first_name, last_name, user_name, attributes='{"attributes" : [ ]}'
    ):
        uri = CREATE_DEVELOPER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name
        )
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = {
            "email": self._developer_email,
            "firstName": first_name,
            "lastName": last_name,
            "userName": user_name,
            "attributes": json.loads(attributes)["attributes"],
        }
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_developer(self):
        uri = DELETE_DEVELOPER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_developer(self):
        uri = GET_DEVELOPER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_developer_by_app(self, app_name):
        uri = GET_DEVELOPER_BY_APP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, app_name=app_name
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_developers(
        self, prefix=None, expand=False, count=1000, startkey="", format="json"
    ):
        uri = LIST_DEVELOPERS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            expand=expand,
            count=count,
            startkey=startkey,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return DevelopersSerializer().serialize_details(resp, format, prefix=prefix)

    def set_developer_status(self, action):
        uri = SET_DEVELOPER_STATUS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
            action=action,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/octet-stream",
            },
        )
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def update_developer(self, request_body):
        uri = UPDATE_DEVELOPER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def get_developer_attribute(self, attribute_name):
        uri = GET_DEVELOPER_ATTRIBUTE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
            attribute_name=attribute_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def update_a_developer_attribute(self, attribute_name, updated_value):
        uri = UPDATE_A_DEVELOPER_ATTRIBUTE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
            attribute_name=attribute_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        body = {"value": updated_value}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_developer_attribute(self, attribute_name):
        uri = DELETE_DEVELOPER_ATTRIBUTE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
            attribute_name=attribute_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_all_developer_attributes(self):
        uri = GET_ALL_DEVELOPER_ATTRIBUTES_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def update_all_developer_attributes(self, request_body):
        uri = UPDATE_ALL_DEVELOPER_ATTRIBUTES_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
        )
        hdrs = auth.set_header(
            self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp
