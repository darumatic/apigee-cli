import argparse

from apigee.api import maskconfigs

from apigee.parsers.parent_parser import ParentParser

class ParserMaskconfigs:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_maskconfigs = self._parser.add_parser('mask', aliases=['maskconfigs'], help='data masks').add_subparsers()
        self._parent_parser = kwargs.get('parent_parser', ParentParser())
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def parser_maskconfigs(self):
        return self._parser_maskconfigs

    @parser_maskconfigs.setter
    def parser_maskconfigs(self, value):
        self._parser_maskconfigs = value

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    def __call__(self):
        return self._parser

    def _build_create_data_masks_for_an_api_proxy_argument(self):
        create_data_masks_for_an_api_proxy = self._parser_maskconfigs.add_parser('create-api', aliases=['create-data-masks-for-an-api-proxy'], parents=[self._parent_parser()],
            help='Create a data mask for an API proxy. You can capture message content to assist in runtime debugging of APIs calls. In many cases, API traffic contains sensitive data, such credit cards or personally identifiable health information (PHI) that needs to filtered out of the captured message content. Data masks enable you to specify data that will be filtered out of trace sessions. Data masking is only enabled when a trace session (also called a \'debug\' session) is enabled for an API proxy. If no trace session are enabled on an API proxy, then the data will not be masked.')
        create_data_masks_for_an_api_proxy.add_argument('-n', '--name', help='name', required=True)
        create_data_masks_for_an_api_proxy.add_argument('-b', '--body', help='request body', required=True)
        create_data_masks_for_an_api_proxy.set_defaults(func=lambda args: print(maskconfigs.create_data_masks_for_an_api_proxy(args).text))

    def _build_delete_data_masks_for_an_api_proxy_argument(self):
        delete_data_masks_for_an_api_proxy = self._parser_maskconfigs.add_parser('delete-api', aliases=['delete-data-masks-for-an-api-proxy'], parents=[self._parent_parser()],
            help='Delete a data mask for an API proxy.')
        delete_data_masks_for_an_api_proxy.add_argument('-n', '--name', help='name', required=True)
        delete_data_masks_for_an_api_proxy.add_argument('--maskconfig-name', help='data mask name', required=True)
        delete_data_masks_for_an_api_proxy.set_defaults(func=lambda args: print(maskconfigs.delete_data_masks_for_an_api_proxy(args).text))

    def _build_get_data_mask_details_for_an_api_proxy_argument(self):
        get_data_mask_details_for_an_api_proxy = self._parser_maskconfigs.add_parser('get-api', aliases=['get-data-mask-details-for-an-api-proxy'], parents=[self._parent_parser()],
            help='Get the details for a data mask for an API proxy.')
        get_data_mask_details_for_an_api_proxy.add_argument('-n', '--name', help='name', required=True)
        get_data_mask_details_for_an_api_proxy.add_argument('--maskconfig-name', help='data mask name', required=True)
        get_data_mask_details_for_an_api_proxy.set_defaults(func=lambda args: print(maskconfigs.get_data_mask_details_for_an_api_proxy(args).text))

    def _build_list_data_masks_for_an_api_proxy_argument(self):
        list_data_masks_for_an_api_proxy = self._parser_maskconfigs.add_parser('list-api', aliases=['list-data-masks-for-an-api-proxy'], parents=[self._parent_parser()],
            help='List all data masks for an API proxy.')
        list_data_masks_for_an_api_proxy.add_argument('-n', '--name', help='name', required=True)
        list_data_masks_for_an_api_proxy.set_defaults(func=lambda args: print(maskconfigs.list_data_masks_for_an_api_proxy(args).text))

    def _build_list_data_masks_for_an_organization_argument(self):
        list_data_masks_for_an_organization = self._parser_maskconfigs.add_parser('list', aliases=['list-data-masks-for-an-organization'], parents=[self._parent_parser()],
            help='List all data masks for an organization.')
        list_data_masks_for_an_organization.set_defaults(func=lambda args: print(maskconfigs.list_data_masks_for_an_organization(args).text))

    def _create_parser(self):
        self._build_create_data_masks_for_an_api_proxy_argument()
        self._build_delete_data_masks_for_an_api_proxy_argument()
        self._build_get_data_mask_details_for_an_api_proxy_argument()
        self._build_list_data_masks_for_an_api_proxy_argument()
        self._build_list_data_masks_for_an_organization_argument()
