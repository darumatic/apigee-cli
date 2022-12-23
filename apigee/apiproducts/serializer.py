import json


class ApiproductsSerializer:
    def serialize_details(self, apiproducts, format, prefix=None):
        resp = apiproducts
        if format == "text":
            return apiproducts.text
        apiproducts = apiproducts.json()
        if prefix:
            apiproducts = [
                apiproduct
                for apiproduct in apiproducts
                if apiproduct.startswith(prefix)
            ]
        if format == "json":
            return json.dumps(apiproducts)
        elif format == "table":
            pass
        elif format == "dict":
            return apiproducts
        return resp
