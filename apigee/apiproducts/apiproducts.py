import json

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.apiproducts.serializer import ApiproductsSerializer
from apigee.utils import read_file_content

CREATE_API_PRODUCT_PATH = "{api_url}/v1/organizations/{org}/apiproducts"
DELETE_API_PRODUCT_PATH = "{api_url}/v1/organizations/{org}/apiproducts/{name}"
GET_API_PRODUCT_PATH = "{api_url}/v1/organizations/{org}/apiproducts/{name}"
LIST_API_PRODUCTS_PATH = "{api_url}/v1/organizations/{org}/apiproducts?expand={expand}&count={count}&startKey={startkey}"
UPDATE_API_PRODUCT_PATH = "{api_url}/v1/organizations/{org}/apiproducts/{name}"


class Apiproducts:
    def __init__(self, auth, org_name, apiproduct_name):
        self.auth = auth
        self.org_name = org_name
        self.apiproduct_name = apiproduct_name

    def create_api_product(self, request_body):
        uri = CREATE_API_PRODUCT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_api_product(self):
        uri = DELETE_API_PRODUCT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, name=self.apiproduct_name
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_api_product(self):  # sourcery skip: class-extract-method
        uri = GET_API_PRODUCT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, name=self.apiproduct_name
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_api_products(
        self, prefix=None, expand=False, count=1000, startkey="", format="json"
    ):
        uri = LIST_API_PRODUCTS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self.org_name,
            expand=expand,
            count=count,
            startkey=startkey,
        )
        hdrs = auth.set_authentication_headers(self.auth, custom_headers={"Accept": "application/json"})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return ApiproductsSerializer().serialize_details(resp, format, prefix=prefix)

    def push_apiproducts(self, file):
        apiproduct = read_file_content(file, type="json")
        self.apiproduct_name = apiproduct["name"]
        try:
            self.get_api_product()
            console.echo(f"Updating {self.apiproduct_name}")
            console.echo(self.update_api_product(json.dumps(apiproduct)).text)
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            console.echo(f"Creating {self.apiproduct_name}")
            console.echo(self.create_api_product(json.dumps(apiproduct)).text)

    def update_api_product(self, request_body):
        uri = UPDATE_API_PRODUCT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self.org_name, name=self.apiproduct_name
        )
        hdrs = auth.set_authentication_headers(
            self.auth,
            custom_headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp
