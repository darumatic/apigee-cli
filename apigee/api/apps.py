#!/usr/bin/env python
"""Source: https://apidocs.apigee.com/api/apps-developer,
https://apidocs.apigee.com/api/developer-app-keys

Apps associated with developers (as developer apps).

Apps are API consumers registered with an API provider's organization.
Apps are registered with an organization to obtain credentials that enable
access to one or more API products (or, a set of URIs). The default app profile
can be extended by using custom attributes.
"""

import json
import random
import requests
import string

from apigee import APIGEE_ADMIN_API_URL
from apigee.abstract.api.apps import IApps, AppsSerializer
from apigee.util import authorization, console


class Apps(IApps):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_developer_app(self, developer, request_body):
        """Creates an app associated with a developer, associates the app with
        an API product, and auto-generates an API key for the app to use in
        calls to API proxies inside the API product.

        The name is the unique ID of the app that you can use in management API
        calls.
        The DisplayName (set with an attribute) is what appears in the
        management UI.
        If you don't provide a DisplayName, the name is used.

        The keyExpiresIn property sets the expiration on the API key.
        If you don't set this, or set the value to -1, they API key never
        expires.

        Apigee recommends that you use the developer's email address when
        calling this API.
        Developer IDs are generated internally by Apigee and are not guaranteed
        to stay the same over time.

        Args:
            developer (str): The developer's email address or ID.
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{developer}/apps"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_developer_app(self, developer):
        """Deletes a developer app.

        Note the following:
          - With Apigee Edge for Public Cloud, deletion of the developer app and
            associated artifacts happens asynchronously.
            The developer app is deleted immediately, but the resources
            associated with that developer app, such as app keys or access
            tokens, may take anywhere from a few seconds to a few minutes to be
            automatically deleted.
          - Apigee recommends that you use the developer's email address when
            calling this API. Developer IDs are generated internally by Apigee
            and are not guaranteed to stay the same over time.

        Args:
            developer (str): The developer's email address or ID.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{developer}/apps/{self._app_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def create_empty_developer_app(self, developer, display_name="", callback_url=""):
        """Creates an empty developer app.

        This method combines three API calls to Apigee:
          1. Create a developer app with the option to specify display name and
             callback URL
          2. Delete default key created for the new developer app
          3. Get the developer details

        Args:
            developer (str): The developer's email address or ID.
            display_name (str, optional): The ``DisplayName`` is what appears in
                the management UI. If you don't provide a ``DisplayName``, the
                ``name`` is used.
            callback_url (str, optional): The callbackUrl is used by OAuth 2.0
                authorization servers to communicate authorization codes back to
                apps.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{developer}/apps"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = {
            "name": self._app_name,
            # "apiProducts": args.products,
            "attributes": [{"name": "DisplayName", "value": display_name}],
            # "scopes" : args.scopes,
            "callbackUrl": callback_url,
        }
        if not display_name:
            del body["attributes"]
        if not callback_url:
            del body["callbackUrl"]
        # body = {k: v for k, v in body.items() if v}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        self.delete_key_for_a_developer_app(
            developer, resp.json()["credentials"][0]["consumerKey"]
        )
        return self.get_developer_app_details(developer)

    def get_developer_app_details(self, developer):
        """Get the profile of a specific developer app.

        All times in the response are UNIX times.

        Note that the response contains a top-level attribute named accessType
        that is no longer used by Apigee.

        Args:
            developer (str): The developer's email address or ID.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{developer}/apps/{self._app_name}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_developer_apps(
        self, developer, prefix=None, expand=False, count=100, startkey=""
    ):
        """Lists all apps created by a developer in an organization, and
        optionally provides an expanded view of the apps.

        All time values in the response are UNIX times.

        You can specify either the developer's email address or Edge ID.

        Args:
            developer (str): The developer's email address or ID.
            prefix (str, optional): Filter results by a prefix string.
                Defaults to None.
            expand (bool, optional): If True, show app details.
                Defaults to False.
            count (int, optional): This parameter can be used with Apigee Edge
                for Public Cloud only.
                Limits the list to the number you specify. The limit is 100.
                Use with the startKey parameter to provide more targeted
                filtering.
            startkey (str, optional): This parameter can be used with Apigee
                Edge for Public Cloud only.
                To filter the keys that are returned, enter the name of a
                company app that the list will start with.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{developer}/apps"
        if expand:
            uri += f"?expand={expand}"
        else:
            uri += f"?count={count}&startKey={startkey}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return AppsSerializer().serialize_details(resp, "json", prefix=prefix)

    def delete_key_for_a_developer_app(self, developer, consumer_key):
        """Deletes a consumer key that belongs to an app, and removes all API
        products associated with the app.

        Once deleted, the consumer key cannot be used to access any APIs.

        Args:
            developer (str): The developer's email address or ID.
            consumer_key (str): Consumer key to delete.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{developer}/apps/{self._app_name}/keys/{consumer_key}"
        hdrs = authorization.set_header({"Accept": "application/json"}, self._auth)
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def create_a_consumer_key_and_secret(
        self,
        developer,
        consumer_key=None,
        consumer_secret=None,
        key_length=32,
        secret_length=32,
        key_suffix=None,
        key_delimiter="-",
        products=[],
    ):
        """Creates a custom consumer key and secret for a developer app.

        This is particularly useful if you want to migrate existing consumer
        keys/secrets to Edge from another system.

        Consumer keys and secrets can contain letters, numbers, underscores,
        and hyphens. No other special characters are allowed.

        Args:
            developer (str): The developer's email address or ID.
            consumer_key (str, optional): Consumer key to create.
            consumer_secret (str, optional): Consumer secret to create.
            key_length (int, optional): Length of the consumer key to generate
                if ``consumer_key`` is not specified.
                Defaults to 32 characters.
            secret_length (int, optional): Length of the consumer secret to
                generate if ``consumer_secret`` is not specified.
                Defaults to 32 characters.
            key_suffix (str, optional): String to append to consumer key.
                Defaults to None.
            key_delimiter (str, optional): String to delimit ``consumer_key``
                and ``key_suffix``.
                Defaults to '-'.
            products (list, optional): List of API Products to add to the
                consumer key and secret.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{developer}/apps/{self._app_name}/keys/create"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        # app = self.get_developer_app_details(developer)
        if not consumer_key:
            consumer_key = "".join(
                random.SystemRandom().choice(string.ascii_letters + string.digits)
                for _ in range(key_length)
            )
        if not consumer_secret:
            consumer_secret = "".join(
                random.SystemRandom().choice(string.ascii_letters + string.digits)
                for _ in range(secret_length)
            )
        if key_suffix:
            consumer_key += key_delimiter
            consumer_key += key_suffix
        body = {"consumerKey": consumer_key, "consumerSecret": consumer_secret}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        if products:
            console.log(resp.text)
            consumer_key = resp.json()["consumerKey"]
            request_body = json.dumps(
                {"apiProducts": products, "attributes": resp.json()["attributes"]}
            )
            console.log("Adding API Products", products, "to consumerKey", consumer_key)
            return self.add_api_product_to_key(developer, consumer_key, request_body)
        return resp

    def add_api_product_to_key(self, developer, consumer_key, request_body):
        """Adds an API product to a developer app key, enabling the app that
        holds the key to access the API resources bundled in the API product.

        You can also use this API to add attributes to the key.

        Args:
            developer (str): The developer's email address or ID.
            consumer_key (str, optional): Consumer key to add the API Product
                to.
            request_body (str): JSON string.

        Returns:
            requests.Response()
        """
        uri = f"{APIGEE_ADMIN_API_URL}/v1/organizations/{self._org_name}/developers/{developer}/apps/{self._app_name}/keys/{consumer_key}"
        hdrs = authorization.set_header(
            {"Accept": "application/json", "Content-Type": "application/json"},
            self._auth,
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def restore_app(self, file):
        """Restore developer app file to Apigee.

        This method combines four different types of API calls to Apigee:
          1. Create a developer app
          2. Delete default key created for the new developer app
          3. For each consumer key and secret pair, add (create) to the new app
          4. Get the developer details

        Args:
            file (str): The file path.

        Returns:
            requests.Response()
        """
        with open(file, "r") as f:
            app = json.loads(f.read())
        self._app_name = app["name"]
        request_body = {}
        request_body["name"] = app["name"]
        request_body["attributes"] = app.get("attributes")
        request_body["scopes"] = app.get("scopes")
        request_body["callbackUrl"] = app.get("callbackUrl")
        request_body = {k: v for k, v in request_body.items() if v}
        resp = self.create_developer_app(app["developerId"], json.dumps(request_body))
        consumer_key = resp.json()["credentials"][0]["consumerKey"]
        self.delete_key_for_a_developer_app(app["developerId"], consumer_key)
        if app["credentials"]:
            for cred in app["credentials"]:
                consumer_key = cred["consumerKey"]
                consumer_secret = cred["consumerSecret"]
                products = [product["apiproduct"] for product in cred["apiProducts"]]
                resp = self.create_a_consumer_key_and_secret(
                    app["developerId"],
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    products=products,
                )
        return self.get_developer_app_details(app["developerId"])
