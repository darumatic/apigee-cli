import argparse

from apigee.api.developers import Developers

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.prefix_parser import PrefixParser

class ParserDevelopers:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_developers = self._parser.add_parser('developers', aliases=['devs'], help='see developers').add_subparsers()
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
    def parser_developers(self):
        return self._parser_developers

    @parser_developers.setter
    def parser_developers(self, value):
        self._parser_developers = value

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

    def _build_list_developers_argument(self):
        list_developers = self._parser_developers.add_parser('list', aliases=['list-developers'], parents=[self._parent_parser(), self._prefix_parser()],
            help='Lists all developers in an organization by email address. This call does not list any company developers who are a part of the designated organization.')
        list_developers.add_argument('--expand', action='store_true',
            help='Set to true to list developers exanded with details.')
        list_developers.add_argument('--count', default=1000, type=int,
            help='Limits the list to the number you specify. Use with the startKey parameter to provide more targeted filtering. The limit is 1000.')
        list_developers.add_argument('--startkey', default='',
            help='To filter the keys that are returned, enter the email of a developer that the list will start with.')
        list_developers.set_defaults(func=lambda args: print(Developers(args, args.org, None).list_developers(prefix=args.prefix, expand=args.expand, count=args.count, startkey=args.startkey)))

    def _build_update_a_developer_attribute_argument(self):
        update_a_developer_attribute = self._parser_developers.add_parser('update-attr', aliases=['update-attribute', 'update-a-developer-attribute'], parents=[self._parent_parser()],
            help='Updates the value of a developer attribute.')
        update_a_developer_attribute.add_argument('-n', '--name', help="the developer's email address", required=True)
        update_a_developer_attribute.add_argument('--attribute-name', help="attribute name", required=True)
        update_a_developer_attribute.add_argument('--updated-value', help="updated value", required=True)
        update_a_developer_attribute.set_defaults(func=lambda args: print(Developers(args, args.org, args.name).update_a_developer_attribute(args.attribute_name, args.updated_value).text))

    def _build_delete_developer_attribute_argument(self):
        delete_developer_attribute = self._parser_developers.add_parser('delete-attr', aliases=['delete-attribute', 'delete-developer-attribute'], parents=[self._parent_parser()],
            help='Deletes a developer attribute.')
        delete_developer_attribute.add_argument('-n', '--name', help="the developer's email address", required=True)
        delete_developer_attribute.add_argument('--attribute-name', help="attribute name", required=True)
        delete_developer_attribute.set_defaults(func=lambda args: print(Developers(args, args.org, args.name).delete_developer_attribute(args.attribute_name).text))

    def _build_get_all_developer_attributes_argument(self):
        get_all_developer_attributes = self._parser_developers.add_parser('get-attrs', aliases=['get-attributes', 'get-all-developer-attributes'], parents=[self._parent_parser()],
            help='Returns a list of all developer attributes.')
        get_all_developer_attributes.add_argument('-n', '--name', help="the developer's email address", required=True)
        get_all_developer_attributes.set_defaults(func=lambda args: print(Developers(args, args.org, args.name).get_all_developer_attributes().text))

    def _build_update_all_developer_attributes_argument(self):
        update_all_developer_attributes = self._parser_developers.add_parser('update-all-attrs', aliases=['update-all-attributes', 'update-all-developer-attributes'], parents=[self._parent_parser()],
            help='Updates or creates developer attributes. This API replaces the current list of attributes with the attributes specified in the request body. This lets you update existing attributes, add new attributes, or delete existing attributes by omitting them from the request body.')
        update_all_developer_attributes.add_argument('-n', '--name', help="the developer's email address", required=True)
        update_all_developer_attributes.add_argument('-b', '--body', help='request body', required=True)
        update_all_developer_attributes.set_defaults(func=lambda args: print(Developers(args, args.org, args.name).update_all_developer_attributes(args.body).text))

    def _create_parser(self):
        self._build_list_developers_argument()
        self._build_update_a_developer_attribute_argument()
        self._build_delete_developer_attribute_argument()
        self._build_get_all_developer_attributes_argument()
        self._build_update_all_developer_attributes_argument()
