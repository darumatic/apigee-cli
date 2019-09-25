#!/usr/bin/env python
"""Source: https://apidocs.apigee.com/api/developers-0

Base Path: https://api.enterprise.apigee.com/v1/o/{org_name}

API Resource Path: /developers

Developers implement client/consumer apps and must be registered with an
organization on Apigee Edge.
"""

import json
import requests

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.developers import IDevelopers, DevelopersSerializer
from apigee.util import authorization


class Developers(IDevelopers):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_developer(
        self, first_name, last_name, user_name, attributes='{"attributes" : [ ]}'
    ):
        """Creates a profile for a developer in an organization.

        Once created, the developer can register an app and receive an API key.

        The developer is always created with a status of active.

        Args:
            first_name (str): The developer's first name.
            last_name (str): The developer's last name.
            user_name (str): The developer's user name.
            attributes (str, optional): JSON string.
                Defaults to '{"attributes" : [ ]}'.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
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
        """Deletes a developer from an organization.

        All apps and API keys associated with the developer are also removed
        from the organization.
        All times in the response are UNIX times.

        To avoid permanently deleting developers and their artifacts, consider
        deactivating developers instead.

        Note the following:
          - With Apigee Edge for Public Cloud, deletion of the developer and
            associated artifacts happens asynchronously.
            The developer is deleted immediately, but the resources associated
            with that developer, such as apps, may take anywhere from a few
            seconds to a few minutes to be automatically deleted.
          - Apigee recommends that you use the developer's email address when
            calling this API.
            Developer IDs are generated internally by Apigee and are not
            guaranteed to stay the same over time.

        Args:
            None

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{self._developer_email}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_developer(self):
        """Returns the profile for a developer by email address or ID.

        All time values are UNIX time values.

        The profile includes the developer's email address, ID, name, and other
        information.

        Note the following:
          - With Apigee Edge for Public Cloud, the response includes only the
            first 100 apps.

        Args:
            None

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{self._developer_email}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_developer_by_app(self, app_name):
        """Gets the developer profile by app name.

        The profile retrieved is for the developer associated with the app in
        the organization.
        All time values are UNIX time values.

        Args:
            app_name (str): The name of the app.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers?app={app_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_developers(self, prefix=None, expand=False, count=100, startkey=""):
        """Lists all developers in an organization by email address.

        This call does not list any company developers who are a part of the
        designated organization.

        With Apigee Edge for Public Cloud:
          - A maximum of 1000 developers are returned per API call.
          - You can paginate the list of companies returned using the
            ``startKey`` and ``count`` query parameters.

        Args:
            prefix (str, optional): Filter results by a prefix string.
                Defaults to None.
            expand (bool, optional): If True, list developers exanded with
                details. Defaults to False.
            count (int, optional): Note: This parameter can be used with
                Apigee Edge for Public Cloud only.
                Limits the list to the number you specify.
                Use with the startKey parameter to provide more targeted
                filtering.
                The limit is 1000.
                Defaults to 100.
            startkey (str, optional): Note: This parameter can be used with
                Apigee Edge for Public Cloud only.
                To filter the keys that are returned, enter the email of a
                developer that the list will start with.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers?expand={expand}&count={count}&startKey={startkey}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return DevelopersSerializer().serialize_details(resp, "json", prefix=prefix)

    def set_developer_status(self, action):
        """Sets a developer's status to active or inactive for a specific
        organization.

        Run this API for each organization where you want to change the
        developer's status.

        By default, the status of a developer is set to active.
        Admins with proper permissions (such as Organization Administrator) can
        change a developer's status using this API call.

        If you set a developer's status to inactive, the API keys assigned to
        the developer's apps are no longer valid even though keys continue to
        show a status of "Approved"
        (in strikethrough text in the management UI).
        Inactive developers, however, can still log into the developer portal
        and create apps. The new keys that get created just won't work.

        Args:
            action (str): Set to ``active`` or ``inactive``.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{self._developer_email}?action={action}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/octet-stream"},
            self._auth,
        )
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def update_developer(self, request_body):
        """Update an existing developer profile.

        To add new values or update existing values, submit the new or updated
        portion of the developer profile along with the rest of the developer
        profile, even if no values are changing.

        To delete attributes from a developer profile, submit the entire profile
        without the attributes that you want to delete.

        Args:
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{self._developer_email}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def get_developer_attribute(self, attribute_name):
        """Returns the value of a developer attribute.

        Args:
            attribute_name (str, optional): The attribute name.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{self._developer_email}/attributes/{attribute_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def update_a_developer_attribute(self, attribute_name, updated_value):
        """Updates the value of a developer attribute.

        Args:
            attribute_name (str, optional): The attribute name to update.
            updated_value (str, optional): The new attribute value.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{self._developer_email}/attributes/{attribute_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        body = {"value": updated_value}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_developer_attribute(self, attribute_name):
        """Deletes a developer attribute.

        Args:
            attribute_name (str, optional): The attribute name to delete.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{self._developer_email}/attributes/{attribute_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_all_developer_attributes(self):
        """Returns a list of all developer attributes.

        Args:
            None

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{self._developer_email}/attributes"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def update_all_developer_attributes(self, request_body):
        """Updates or creates developer attributes.

        This API replaces the current list of attributes with the attributes
        specified in the request body.
        This lets you update existing attributes, add new attributes, or delete
        existing attributes by omitting them from the request body.

        Args:
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{self._developer_email}/attributes"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp
