import argparse

from apigee.api.keyvaluemaps import Keyvaluemaps

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.file_parser import FileParser
from apigee.parsers.environment_parser import EnvironmentParser
from apigee.parsers.prefix_parser import PrefixParser

class ParserKeyvaluemaps:

    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_keyvaluemaps = self._parser.add_parser('keyvaluemaps', aliases=['kvms'], help='manage keyvaluemaps').add_subparsers()
        self._parent_parser = kwargs.get('parent_parser', ParentParser())
        self._file_parser = kwargs.get('file_parser', FileParser())
        self._environment_parser = kwargs.get('environment_parser', EnvironmentParser())
        self._prefix_parser = kwargs.get('prefix_parser', PrefixParser(profile='default'))
        self._create_parser()

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    @property
    def parser_keyvaluemaps(self):
        return self._parser_keyvaluemaps

    @parser_keyvaluemaps.setter
    def parser_keyvaluemaps(self, value):
        self._parser_keyvaluemaps = value

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    @property
    def file_parser(self):
        return self._file_parser

    @file_parser.setter
    def file_parser(self, value):
        self._file_parser = value

    @property
    def environment_parser(self):
        return self._environment_parser

    @environment_parser.setter
    def environment_parser(self, value):
        self._environment_parser = value

    @property
    def prefix_parser(self):
        return self._prefix_parser

    @prefix_parser.setter
    def prefix_parser(self, value):
        self._prefix_parser = value

    def __call__(self):
        return self._parser

    def _build_create_keyvaluemap_in_an_environment_argument(self):
        create_keyvaluemap_in_an_environment = self._parser_keyvaluemaps.add_parser('create', aliases=['create-keyvaluemap-in-an-environment'], parents=[self._parent_parser(), self._environment_parser()],
            help='Creates a key value map in an environment.')
        create_keyvaluemap_in_an_environment.add_argument('-b', '--body', help='request body', required=True)
        create_keyvaluemap_in_an_environment.set_defaults(func=lambda args: print(Keyvaluemaps(args, args.org, args.name).create_keyvaluemap_in_an_environment(args.environment, args.body).text))

    def _build_delete_keyvaluemap_from_an_environment_argument(self):
        delete_keyvaluemap_from_an_environment = self._parser_keyvaluemaps.add_parser('delete', aliases=['delete-keyvaluemap-from-an-environment'], parents=[self._parent_parser(), self._environment_parser()],
            help='Deletes a key/value map and all associated entries from an environment.')
        delete_keyvaluemap_from_an_environment.add_argument('-n', '--name', help='name', required=True)
        delete_keyvaluemap_from_an_environment.set_defaults(func=lambda args: print(Keyvaluemaps(args, args.org, args.name).delete_keyvaluemap_from_an_environment(args.environment).text))

    def _build_delete_keyvaluemap_entry_in_an_environment_argument(self):
        delete_keyvaluemap_entry_in_an_environment = self._parser_keyvaluemaps.add_parser('delete-entry', aliases=['delete-keyvaluemap-entry-in-an-environment'], parents=[self._parent_parser(), self._environment_parser()],
            help='Deletes a specific key/value map entry in an environment by name, along with associated entries.')
        delete_keyvaluemap_entry_in_an_environment.add_argument('-n', '--name', help='name', required=True)
        delete_keyvaluemap_entry_in_an_environment.add_argument('--entry-name', help='entry name', required=True)
        delete_keyvaluemap_entry_in_an_environment.set_defaults(func=lambda args: print(Keyvaluemaps(args, args.org, args.name).delete_keyvaluemap_entry_in_an_environment(args.environment, args.entry_name).text))

    def _build_get_keyvaluemap_in_an_environment_argument(self):
        get_keyvaluemap_in_an_environment = self._parser_keyvaluemaps.add_parser('get', aliases=['get-keyvaluemap-in-an-environment'], parents=[self._parent_parser(), self._environment_parser()],
            help='Gets a KeyValueMap (KVM) in an environment by name, along with the keys and values.')
        get_keyvaluemap_in_an_environment.add_argument('-n', '--name', help='name', required=True)
        get_keyvaluemap_in_an_environment.set_defaults(func=lambda args: print(Keyvaluemaps(args, args.org, args.name).get_keyvaluemap_in_an_environment(args.environment).text))

    def _build_get_a_keys_value_in_an_environment_scoped_keyvaluemap_argument(self):
        get_a_keys_value_in_an_environment_scoped_keyvaluemap = self._parser_keyvaluemaps.add_parser('get-value', aliases=['get-a-keys-value-in-an-environment-scoped-keyvaluemap'], parents=[self._parent_parser(), self._environment_parser()],
            help='Gets the value of a key in an environment-scoped KeyValueMap (KVM).')
        get_a_keys_value_in_an_environment_scoped_keyvaluemap.add_argument('-n', '--name', help='name', required=True)
        get_a_keys_value_in_an_environment_scoped_keyvaluemap.add_argument('--entry-name', help='entry name', required=True)
        get_a_keys_value_in_an_environment_scoped_keyvaluemap.set_defaults(func=lambda args: print(Keyvaluemaps(args, args.org, args.name).get_a_keys_value_in_an_environment_scoped_keyvaluemap(args.environment, args.entry_name).text))

    def _build_list_keyvaluemaps_in_an_environment_argument(self):
        list_keyvaluemaps_in_an_environment = self._parser_keyvaluemaps.add_parser('list', aliases=['list-keyvaluemaps-in-an-environment'], parents=[self._parent_parser(), self._environment_parser(), self._prefix_parser()],
            help='Lists the name of all key/value maps in an environment and optionally returns an expanded view of all key/value maps for the environment.')
        list_keyvaluemaps_in_an_environment.set_defaults(func=lambda args: print(Keyvaluemaps(args, args.org, None).list_keyvaluemaps_in_an_environment(args.environment, prefix=args.prefix)))

    def _build_update_keyvaluemap_in_an_environment_argument(self):
        update_keyvaluemap_in_an_environment = self._parser_keyvaluemaps.add_parser('update', aliases=['update-keyvaluemap-in-an-environment'], parents=[self._parent_parser(), self._environment_parser()],
            help='Note: This API is supported for Apigee Edge for Private Cloud only. For Apigee Edge for Public Cloud use Update an entry in an environment-scoped KVM. Updates an existing KeyValueMap in an environment. Does not override the existing map. Instead, this method updates the entries if they exist or adds them if not. It can take several minutes before the new value is visible to runtime traffic.')
        update_keyvaluemap_in_an_environment.add_argument('-n', '--name', help='name', required=True)
        update_keyvaluemap_in_an_environment.add_argument('-b', '--body', help='request body', required=True)
        update_keyvaluemap_in_an_environment.set_defaults(func=lambda args: print(Keyvaluemaps(args, args.org, args.name).update_keyvaluemap_in_an_environment(args.environment, args.body).text))

    def _build_create_an_entry_in_an_environment_scoped_kvm_argument(self):
        create_an_entry_in_an_environment_scoped_kvm = self._parser_keyvaluemaps.add_parser('create-entry', aliases=['create-an-entry-in-an-environment-scoped-kvm'], parents=[self._parent_parser(), self._environment_parser()],
            help='Note: This API is supported for Apigee Edge for the Public Cloud only. Creates an entry in an existing KeyValueMap scoped to an environment. A key (name) cannot be larger than 2 KB. KVM names are case sensitive.')
        create_an_entry_in_an_environment_scoped_kvm.add_argument('-n', '--name', help='name', required=True)
        create_an_entry_in_an_environment_scoped_kvm.add_argument('--entry-name', help='entry name', required=True)
        create_an_entry_in_an_environment_scoped_kvm.add_argument('--entry-value', help='entry value', required=True)
        create_an_entry_in_an_environment_scoped_kvm.set_defaults(func=lambda args: print(Keyvaluemaps(args, args.org, args.name).create_an_entry_in_an_environment_scoped_kvm(args.environment, args.entry_name, args.entry_value).text))

    def _build_update_an_entry_in_an_environment_scoped_kvm_argument(self):
        update_an_entry_in_an_environment_scoped_kvm = self._parser_keyvaluemaps.add_parser('update-entry', aliases=['update-an-entry-in-an-environment-scoped-kvm'], parents=[self._parent_parser(), self._environment_parser()],
            help='Note: This API is supported for Apigee Edge for the Public Cloud only. Updates an entry in a KeyValueMap scoped to an environment. A key cannot be larger than 2 KB. KVM names are case sensitive. Does not override the existing map. It can take several minutes before the new value is visible to runtime traffic.')
        update_an_entry_in_an_environment_scoped_kvm.add_argument('-n', '--name', help='name', required=True)
        update_an_entry_in_an_environment_scoped_kvm.add_argument('--entry-name', help='entry name', required=True)
        update_an_entry_in_an_environment_scoped_kvm.add_argument('--updated-value', help='updated value', required=True)
        update_an_entry_in_an_environment_scoped_kvm.set_defaults(func=lambda args: print(Keyvaluemaps(args, args.org, args.name).update_an_entry_in_an_environment_scoped_kvm(args.environment, args.entry_name, args.updated_value).text))

    def _build_list_keys_in_an_environment_scoped_keyvaluemap_argument(self):
        list_keys_in_an_environment_scoped_keyvaluemap = self._parser_keyvaluemaps.add_parser('list-keys', aliases=['list-keys-in-an-environment-scoped-keyvaluemap'], parents=[self._parent_parser(), self._environment_parser(), self._prefix_parser()],
            help='Note: This API is supported for Apigee Edge for the Public Cloud only. Lists keys in a KeyValueMap scoped to an environment. KVM names are case sensitive.')
        list_keys_in_an_environment_scoped_keyvaluemap.add_argument('-n', '--name', help='name', required=True)
        list_keys_in_an_environment_scoped_keyvaluemap.add_argument('--startkey', default='',
            help='To filter the keys that are returned, enter the name of a key that the list will start with.')
        list_keys_in_an_environment_scoped_keyvaluemap.add_argument('--count', default=100, type=int,
            help='Limits the list of keys to the number you specify, up to a maximum of 100. Use with the startkey parameter to provide more targeted filtering.')
        list_keys_in_an_environment_scoped_keyvaluemap.set_defaults(func=lambda args: print(Keyvaluemaps(args, args.org, args.name).list_keys_in_an_environment_scoped_keyvaluemap(args.environment, args.startkey, args.count).text))

    def _build_push_keyvaluemap_argument(self):
        push_keyvaluemap = self._parser_keyvaluemaps.add_parser('push', aliases=['push-keyvaluemap'], parents=[self._parent_parser(), self._environment_parser(), self._file_parser()],
            help='Push KeyValueMap to Apigee. This will create KeyValueMap/entries if they do not exist, update existing KeyValueMap/entries, and delete entries on Apigee that are not present in the request body.')
        # push_keyvaluemap.add_argument('-n', '--name', help='name', required=True)
        push_keyvaluemap.set_defaults(func=lambda args: Keyvaluemaps(args, args.org, None).push_keyvaluemap(args.environment, args.file))

    def _create_parser(self):
        self._build_create_keyvaluemap_in_an_environment_argument()
        self._build_delete_keyvaluemap_from_an_environment_argument()
        self._build_delete_keyvaluemap_entry_in_an_environment_argument()
        self._build_get_keyvaluemap_in_an_environment_argument()
        self._build_get_a_keys_value_in_an_environment_scoped_keyvaluemap_argument()
        self._build_list_keyvaluemaps_in_an_environment_argument()
        self._build_update_keyvaluemap_in_an_environment_argument()
        self._build_create_an_entry_in_an_environment_scoped_kvm_argument()
        self._build_update_an_entry_in_an_environment_scoped_kvm_argument()
        self._build_list_keys_in_an_environment_scoped_keyvaluemap_argument()
        self._build_push_keyvaluemap_argument()
