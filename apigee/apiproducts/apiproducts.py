import json

import requests
from requests.exceptions import HTTPError

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.apiproducts.serializer import ApiproductsSerializer
from apigee.utils import read_file

CREATE_API_PRODUCT_PATH = '{api_url}/v1/organizations/{org}/apiproducts'
DELETE_API_PRODUCT_PATH = '{api_url}/v1/organizations/{org}/apiproducts/{name}'
GET_API_PRODUCT_PATH = '{api_url}/v1/organizations/{org}/apiproducts/{name}'
LIST_API_PRODUCTS_PATH = (
    '{api_url}/v1/organizations/{org}/apiproducts?expand={expand}&count={count}&startKey={startkey}'
)
UPDATE_API_PRODUCT_PATH = '{api_url}/v1/organizations/{org}/apiproducts/{name}'


class Apiproducts:
    def __init__(self, auth, org_name, apiproduct_name):
        self._auth = auth
        self._org_name = org_name
        self._apiproduct_name = apiproduct_name

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

    @property
    def apiproduct_name(self):
        return self._apiproduct_name

    @apiproduct_name.setter
    def apiproduct_name(self, value):
        self._apiproduct_name = value

    def create_api_product(self, request_body):
        uri = CREATE_API_PRODUCT_PATH.format(api_url=APIGEE_ADMIN_API_URL, org=self._org_name)
        hdrs = auth.set_header(
            self._auth, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}
        )
        body = json.loads(request_body)
        resp = requests.post(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def delete_api_product(self):
        uri = DELETE_API_PRODUCT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, name=self._apiproduct_name
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.delete(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def get_api_product(self):
        uri = GET_API_PRODUCT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, name=self._apiproduct_name
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return resp

    def list_api_products(self, prefix=None, expand=False, count=1000, startkey="", format='json'):
        uri = LIST_API_PRODUCTS_PATH.format(
            api_url=APIGEE_ADMIN_API_URL,
            org=self._org_name,
            expand=expand,
            count=count,
            startkey=startkey,
        )
        hdrs = auth.set_header(self._auth, headers={'Accept': 'application/json'})
        resp = requests.get(uri, headers=hdrs)
        resp.raise_for_status()
        return ApiproductsSerializer().serialize_details(resp, format, prefix=prefix)

    def update_api_product(self, request_body):
        uri = UPDATE_API_PRODUCT_PATH.format(
            api_url=APIGEE_ADMIN_API_URL, org=self._org_name, name=self._apiproduct_name
        )
        hdrs = auth.set_header(
            self._auth, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}
        )
        body = json.loads(request_body)
        resp = requests.put(uri, headers=hdrs, json=body)
        resp.raise_for_status()
        return resp

    def push_apiproducts(self, file):
        apiproduct = read_file(file, type='json')
        self._apiproduct_name = apiproduct['name']
        try:
            self.get_api_product()
            console.echo(f'Updating {self._apiproduct_name}')
            console.echo(self.update_api_product(body).text)
        except HTTPError as e:
            if e.response.status_code != 404:
                raise e
            console.echo(f'Creating {self._apiproduct_name}')
            console.echo(self.create_api_product(body).text)
