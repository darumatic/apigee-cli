import json

import requests

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
        return self._extracted_from_update_all_developer_attributes_18(uri, hdrs, body)

    def delete_developer(self):
        uri = DELETE_DEVELOPER_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
        )
        return self._extracted_from_delete_developer_attribute_7(uri)

    def get_developer(self):
        return self._extracted_from_get_all_developer_attributes_2(GET_DEVELOPER_PATH)

    def get_developer_by_app(self, app_name):
        uri = GET_DEVELOPER_BY_APP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, app_name=app_name
        )
        return self._extracted_from_get_all_developer_attributes_7(uri)

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
        resp = self._extracted_from_get_all_developer_attributes_7(uri)
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
        return self._extracted_from_get_all_developer_attributes_7(uri)

    def update_a_developer_attribute(self, attribute_name, updated_value):
        uri = UPDATE_A_DEVELOPER_ATTRIBUTE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
            attribute_name=attribute_name,
        )
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        body = {"value": updated_value}
        return self._extracted_from_update_all_developer_attributes_18(uri, hdrs, body)

    def delete_developer_attribute(self, attribute_name):
        uri = DELETE_DEVELOPER_ATTRIBUTE_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
            attribute_name=attribute_name,
        )
        return self._extracted_from_delete_developer_attribute_7(uri)

    # TODO Rename this here and in `delete_developer` and `delete_developer_attribute`
    def _extracted_from_delete_developer_attribute_7(self, uri):
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_all_developer_attributes(self):
        return self._extracted_from_get_all_developer_attributes_2(
            GET_ALL_DEVELOPER_ATTRIBUTES_PATH
        )

    # TODO Rename this here and in `get_developer`, `get_developer_by_app`, `list_developers`, `get_developer_attribute` and `get_all_developer_attributes`
    def _extracted_from_get_all_developer_attributes_2(self, arg0):
        uri = arg0.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            developer_email=self._developer_email,
        )
        return self._extracted_from_get_all_developer_attributes_7(uri)

    # TODO Rename this here and in `get_developer`, `get_developer_by_app`, `list_developers`, `get_developer_attribute` and `get_all_developer_attributes`
    def _extracted_from_get_all_developer_attributes_7(self, uri):
        hdrs = auth.set_header(self._auth, headers={"Accept": "application/json"})
        result = requests.get(uri, headers=hdrs)
        result.raise_for_status()
        return result

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
        return self._extracted_from_update_all_developer_attributes_18(uri, hdrs, body)

    # TODO Rename this here and in `create_developer`, `update_a_developer_attribute` and `update_all_developer_attributes`
    def _extracted_from_update_all_developer_attributes_18(self, uri, hdrs, body):
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp
