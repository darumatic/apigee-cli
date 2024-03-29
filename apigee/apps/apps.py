import json
import random
import string

import requests

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.apps.serializer import AppsSerializer

GET_ORGANIZATION_APP_PATH = "{api_url}/v1/organizations/{org}/apps/{name}"
LIST_ORGANIZATION_APPS_PATH = "{api_url}/v1/organizations/{org}/apps"
CREATE_DEVELOPER_APP_PATH = "{api_url}/v1/organizations/{org}/developers/{developer}/apps"
DELETE_DEVELOPER_APP_PATH = "{api_url}/v1/organizations/{org}/developers/{developer}/apps/{name}"
CREATE_EMPTY_DEVELOPER_APP_PATH = CREATE_DEVELOPER_APP_PATH
GET_DEVELOPER_APP_DETAILS_PATH = "{api_url}/v1/organizations/{org}/developers/{developer}/apps/{name}"
LIST_DEVELOPER_APPS_PATH = "{api_url}/v1/organizations/{org}/developers/{developer}/apps"
DELETE_KEY_FOR_A_DEVELOPER_APP_PATH = "{api_url}/v1/organizations/{org}/developers/{developer}/apps/{name}/keys/{consumer_key}"
CREATE_A_CONSUMER_KEY_AND_SECRET_PATH = "{api_url}/v1/organizations/{org}/developers/{developer}/apps/{name}/keys/create"
ADD_API_PRODUCT_TO_KEY_PATH = "{api_url}/v1/organizations/{org}/developers/{developer}/apps/{name}/keys/{consumer_key}"
UPDATE_KEY_FOR_A_DEVELOPER_APP_PATH = "{api_url}/v1/organizations/{org}/developers/{developer}/apps/{name}/keys/{consumer_key}"


class Apps:
    def __init__(self, auth, org_name, app_name):
        self.auth = auth
        self.org_name = org_name
        self.app_name = app_name

    def add_api_product_to_key(self, developer, consumer_key, request_body):
        uri = ADD_API_PRODUCT_TO_KEY_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            developer=developer,
            name=self.app_name,
            consumer_key=consumer_key,
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
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
        uri = CREATE_A_CONSUMER_KEY_AND_SECRET_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            developer=developer,
            name=self.app_name,
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        # app = self.get_developer_app_details(developer)
        def _rand(length):
            return "".join(
                random.SystemRandom().choice(string.ascii_letters + string.digits)
                for _ in range(length)
            )

        if not consumer_key:
            consumer_key = _rand(key_length)
        if not consumer_secret:
            consumer_secret = _rand(secret_length)
        if key_suffix:
            consumer_key += key_delimiter
            consumer_key += key_suffix
        body = {"consumerKey": consumer_key, "consumerSecret": consumer_secret}
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        if products:
            console.echo(resp.text)
            consumer_key = resp.json()["consumerKey"]
            request_body = json.dumps(
                {"apiProducts": products, "attributes": resp.json()["attributes"]}
            )
            console.echo(
                f"Adding API Products {products} to consumerKey {consumer_key}"
            )
            return self.add_api_product_to_key(developer, consumer_key, request_body)
        return resp

    def create_developer_app(self, developer, request_body):
        # sourcery skip: class-extract-method
        uri = CREATE_DEVELOPER_APP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, developer=developer
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def create_empty_developer_app(self, developer, display_name="", callback_url=""):
        uri = CREATE_EMPTY_DEVELOPER_APP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, developer=developer
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = {
            "name": self.app_name,
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

    def delete_developer_app(self, developer):
        uri = DELETE_DEVELOPER_APP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            developer=developer,
            name=self.app_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def delete_key_for_a_developer_app(self, developer, consumer_key):
        uri = DELETE_KEY_FOR_A_DEVELOPER_APP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            developer=developer,
            name=self.app_name,
            consumer_key=consumer_key,
        )
        hdrs = auth.set_authentication_headers(self.auth, {"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_developer_app_details(self, developer):
        uri = GET_DEVELOPER_APP_DETAILS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            developer=developer,
            name=self.app_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_org_app(self):
        uri = GET_ORGANIZATION_APP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, name=self.app_name,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_apps_for_all_developers(
        self,
        list_of_developers,
        prefix=None,
        expand=False,
        count=1000,
        startkey="",
        format="dict",
        progress_bar=False,
    ):
        return {
            developer: self.list_developer_apps(
                developer,
                prefix=prefix,
                expand=expand,
                count=count,
                startkey=startkey,
                format=format,
            )
            for developer in list_of_developers
        }

    def list_developer_apps(
        self,
        developer,
        prefix=None,
        expand=False,
        count=1000,
        startkey="",
        format="json",
    ):
        uri = LIST_DEVELOPER_APPS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, developer=developer
        )
        uri += f"?expand={expand}" if expand else f"?count={count}&startKey={startkey}"
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return AppsSerializer().serialize_details(resp, format, prefix=prefix)

    def list_org_apps(self, apptype, expand, rows, startkey, status):
        uri = LIST_ORGANIZATION_APPS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name,
        )

        params = {}
        if apptype:
            params['apptype'] = apptype
        if expand:
            params['expand'] = 'true'
        if rows:
            params['rows'] = rows
        if startkey:
            params['startKey'] = startkey
        if status:
            params['status'] = status

        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs, params=params)
        resp.raise_for_status()
        return resp

    def restore_and_update_app_details(self, file):
        with open(file, "r") as f:
            app = json.loads(f.read())
        self.app_name = app["name"]
        request_body = {"name": app["name"], "attributes": app.get("attributes")}
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

    def update_key_for_a_developer_app(self, developer, consumer_key, action):
        uri = UPDATE_KEY_FOR_A_DEVELOPER_APP_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            developer=developer,
            name=self.app_name,
            consumer_key=consumer_key,
        )
        uri += f"?action={action}"

        hdrs = auth.set_authentication_headers(self.auth, {"Content-Type": "application/octet-stream"})
        resp = requests.post(uri, headers=hdrs)
        resp.raise_for_status()
        return resp
