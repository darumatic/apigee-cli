import argparse

from apigee.api import apiproducts

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.prefix_parser import PrefixParser

class ParserApiproducts:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_apiproducts = self._parser.add_parser('products', aliases=['prods'], help='api products').add_subparsers()
        self._parent_parser = kwargs.get('parent_parser', ParentParser())
        self._prefix_parser = kwargs.get('prefix_parser', PrefixParser(profile='default'))
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def parser_apiproducts(self):
        return self._parser_apiproducts

    @parser_apiproducts.setter
    def parser_apiproducts(self, value):
        self._parser_apiproducts = value

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    @property
    def prefix_parser(self):
        return self._prefix_parser

    @prefix_parser.setter
    def prefix_parser(self, value):
        self._prefix_parser = value

    def __call__(self):
        return self._parser

    def _build_list_api_products_argument(self):
        list_api_products = self._parser_apiproducts.add_parser('list', aliases=['list-api-products'], parents=[self._parent_parser(), self._prefix_parser()],
            help='Get a list of all API product names for an organization.')
        list_api_products.add_argument('--expand', action='store_true',
            help='Set to \'true\' to get expanded details about each product.')
        list_api_products.add_argument('--count', default=1000, type=int,
            help='Number of API products to return in the API call. The maximum limit is 1000. Use with the startkey to provide more targeted filtering.')
        list_api_products.add_argument('--startkey', default='',
            help='Returns a list of API products starting with the specified API product.')
        list_api_products.set_defaults(func=lambda args: print(apiproducts.list_api_products(args)))

    def _build_get_api_product_argument(self):
        get_api_product = self._parser_apiproducts.add_parser('get', aliases=['get-api-product'], parents=[self._parent_parser()],
            help='Gets configuration data for an API product. The API product name required in the request URL is not the "Display Name" value displayed for the API product in the Edge UI. While they may be the same, they are not always the same depending on whether the API product was created via UI or API.')
        get_api_product.add_argument('-n', '--name', help='name', required=True)
        get_api_product.set_defaults(func=lambda args: print(apiproducts.get_api_product(args).text))

    def _create_parser(self):
        self._build_list_api_products_argument()
        self._build_get_api_product_argument()
