import argparse

from apigee.api.apps import Apps

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.prefix_parser import PrefixParser

class ParserApps:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_apps = self._parser.add_parser('apps', help='manage developer apps').add_subparsers()
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
    def parser_apps(self):
        return self._parser_apps

    @parser_apps.setter
    def parser_apps(self, value):
        self._parser_apps = value

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

    def _build_create_developer_app_argument(self):
        create_developer_app = self._parser_apps.add_parser('create', aliases=['create-developer-app'], parents=[self._parent_parser()],
            help='Creates an app associated with a developer, associates the app with an API product, and auto-generates an API key for the app to use in calls to API proxies inside the API product.')
        create_developer_app.add_argument('-d', '--developer', help='developer email or id', required=True)
        create_developer_app.add_argument('-b', '--body', help='request body', required=True)
        create_developer_app.set_defaults(func=lambda args: print(Apps(args, args.org, None).create_developer_app(args.developer, args.body).text))

    def _build_create_empty_developer_app_argument(self):
        create_empty_developer_app = self._parser_apps.add_parser('create-empty', aliases=['create-empty-developer-app'], parents=[self._parent_parser()],
            help='Creates an empty developer app.')
        create_empty_developer_app.add_argument('-d', '--developer', help='developer email or id', required=True)
        create_empty_developer_app.add_argument('-n', '--name', help='Name of the app. The name is the unique ID of the app for this organization and developer.', required=True)
        # create_empty_developer_app.add_argument('--products', help='A list of API products associated with the app\'s credentials', nargs='+', required=False, default=[])
        create_empty_developer_app.add_argument('--display-name', help='The DisplayName (set with an attribute) is what appears in the management UI. If you don\'t provide a DisplayName, the name is used.', required=False, default=None)
        # create_empty_developer_app.add_argument('--scopes', help='Sets the scopes element under the apiProducts element in the attributes of the app. The specified scopes must already exist on the API products associated with the app.', nargs='+', required=False, default=[])
        create_empty_developer_app.add_argument('--callback-url', help='The callbackUrl is used by OAuth 2.0 authorization servers to communicate authorization codes back to apps. CallbackUrl must match the value of redirect_uri in some OAuth 2.0 See the documentation on OAuth 2.0 for more details.', required=False, default=None)
        create_empty_developer_app.set_defaults(func=lambda args: print(Apps(args, args.org, args.name).create_empty_developer_app(args.developer, display_name=args.display_name, callback_url=args.callback_url).text))

    def _build_create_a_consumer_key_and_secret_argument(self):
        create_a_consumer_key_and_secret = self._parser_apps.add_parser('create-creds', aliases=['create-a-consumer-key-and-secret', 'create-credentials'], parents=[self._parent_parser()],
            help='Creates a custom consumer key and secret for a developer app. This is particularly useful if you want to migrate existing consumer keys/secrets to Edge from another system. Consumer keys and secrets can contain letters, numbers, underscores, and hyphens. No other special characters are allowed.')
        create_a_consumer_key_and_secret.add_argument('-d', '--developer', help='developer email or id', required=True)
        create_a_consumer_key_and_secret.add_argument('-n', '--name', help='Name of the app. The name is the unique ID of the app for this organization and developer.', required=True)
        create_a_consumer_key_and_secret.add_argument('--consumer-key', help='', required=False, default=None)
        create_a_consumer_key_and_secret.add_argument('--consumer-secret', help='', required=False, default=None)
        create_a_consumer_key_and_secret.add_argument('--key-length', help='length of consumer key', required=False, type=int, default=32)
        create_a_consumer_key_and_secret.add_argument('--secret-length', help='length of consumer secret', required=False, type=int, default=32)
        create_a_consumer_key_and_secret.add_argument('--key-suffix', help='', required=False, default=None)
        create_a_consumer_key_and_secret.add_argument('--key-delimiter', help="separates consumerKey and key suffix with a delimiter. the default is '-'.", required=False, default='-')
        create_a_consumer_key_and_secret.add_argument('--products', help='A list of API products to be associated with the app\'s credentials', nargs='+', required=False, default=[])
        create_a_consumer_key_and_secret.set_defaults(func=lambda args: print(Apps(args, args.org, args.name).create_a_consumer_key_and_secret(args.developer, consumer_key=args.consumer_key, consumer_secret=args.consumer_secret, key_length=args.key_length, secret_length=args.secret_length, key_suffix=args.key_suffix, key_delimiter=args.key_delimiter, products=args.products).text))

    def _build_list_developer_apps_argument(self):
        list_developer_apps = self._parser_apps.add_parser('list', aliases=['list-developer-apps'], parents=[self._parent_parser(), self._prefix_parser()],
            help='Lists all apps created by a developer in an organization, and optionally provides an expanded view of the apps. All time values in the response are UNIX times. You can specify either the developer\'s email address or Edge ID.')
        list_developer_apps.add_argument('-d', '--developer', help='developer email or id', required=True)
        list_developer_apps.add_argument('--expand', action='store_true',
            help='Set to true to expand the results. This query parameter does not work if you use the count or startKey query parameters.')
        list_developer_apps.add_argument('--count', default=100, type=int,
            help='Limits the list to the number you specify. The limit is 100. Use with the startKey parameter to provide more targeted filtering.')
        list_developer_apps.add_argument('--startkey', default='',
            help='To filter the keys that are returned, enter the name of a company app that the list will start with.')
        list_developer_apps.set_defaults(func=lambda args: print(Apps(args, args.org, None).list_developer_apps(args.developer, prefix=args.prefix, expand=args.expand, count=args.count, startkey=args.startkey)))

    def _build_get_developer_app_details_argument(self):
        get_developer_app_details = self._parser_apps.add_parser('get', aliases=['get-developer-app-details'], parents=[self._parent_parser()],
            help='Get the profile of a specific developer app. All times in the response are UNIX times. Note that the response contains a top-level attribute named accessType that is no longer used by Apigee.')
        get_developer_app_details.add_argument('-d', '--developer', help='developer email or id', required=True)
        get_developer_app_details.add_argument('-n', '--name', help='name', required=True)
        get_developer_app_details.set_defaults(func=lambda args: print(Apps(args, args.org, args.name).get_developer_app_details(args.developer).text))

    def _create_parser(self):
        self._build_create_developer_app_argument()
        self._build_create_empty_developer_app_argument()
        self._build_create_a_consumer_key_and_secret_argument()
        self._build_list_developer_apps_argument()
        self._build_get_developer_app_details_argument()
