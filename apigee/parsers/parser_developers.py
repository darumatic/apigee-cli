import argparse

from apigee.api.developers import Developers

from apigee.parsers.parent_parser import ParentParser
from apigee.parsers.prefix_parser import PrefixParser
from apigee.parsers.silent_parser import SilentParser
from apigee.parsers.verbose_parser import VerboseParser

from apigee.util import console


class ParserDevelopers:
    def __init__(self, parser, **kwargs):
        self._parser = parser
        self._parser_developers = self._parser.add_parser(
            "developers", aliases=["devs"], help="manage developers"
        ).add_subparsers()
        self._parent_parser = kwargs.get("parent_parser", ParentParser())
        self._prefix_parser = kwargs.get(
            "prefix_parser", PrefixParser(profile="default")
        )
        self._silent_parser = kwargs.get("silent_parser", SilentParser())
        self._verbose_parser = kwargs.get("verbose_parser", VerboseParser())
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

    def _build_create_developer_argument(self):
        create_developer = self._parser_developers.add_parser(
            "create",
            aliases=["create-developer"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._prefix_parser(),
            ],
            help="Creates a profile for a developer in an organization. Once created, the developer can register an app and receive an API key.",
        )
        create_developer.add_argument(
            "-n",
            "--name",
            help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
            required=True,
        )
        create_developer.add_argument(
            "--first-name", help="The first name of the developer.", required=True
        )
        create_developer.add_argument(
            "--last-name", help="The last name of the developer.", required=True
        )
        create_developer.add_argument(
            "--user-name",
            help="The developer's username. This value is not used by Apigee Edge.",
            required=True,
        )
        create_developer.add_argument(
            "--attributes",
            help="request body e.g.: '{\"attributes\" : [ ]}'",
            required=False,
            default='{"attributes" : [ ]}',
        )
        create_developer.set_defaults(
            func=lambda args: console.log(
                Developers(args, args.org, args.name)
                .create_developer(
                    args.first_name,
                    args.last_name,
                    args.user_name,
                    attributes=args.attributes,
                )
                .text
            )
        )

    def _build_delete_developer_argument(self):
        delete_developer = self._parser_developers.add_parser(
            "delete",
            aliases=["delete-developer"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._prefix_parser(),
            ],
            help="Deletes a developer from an organization. All apps and API keys associated with the developer are also removed from the organization. All times in the response are UNIX times. To avoid permanently deleting developers and their artifacts, consider deactivating developers instead.",
        )
        delete_developer.add_argument(
            "-n",
            "--name",
            help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
            required=True,
        )
        delete_developer.set_defaults(
            func=lambda args: console.log(
                Developers(args, args.org, args.name).delete_developer().text
            )
        )

    def _build_get_developer_argument(self):
        get_developer = self._parser_developers.add_parser(
            "get",
            aliases=["get-developer"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._prefix_parser(),
            ],
            help="Returns the profile for a developer by email address or ID. All time values are UNIX time values. The profile includes the developer's email address, ID, name, and other information.",
        )
        get_developer.add_argument(
            "-n",
            "--name",
            help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
            required=True,
        )
        get_developer.set_defaults(
            func=lambda args: console.log(
                Developers(args, args.org, args.name).get_developer().text
            )
        )

    def _build_get_developer_by_app_argument(self):
        get_developer_by_app = self._parser_developers.add_parser(
            "get-by-app",
            aliases=["get-developer-by-app"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._prefix_parser(),
            ],
            help="Gets the developer profile by app name. The profile retrieved is for the developer associated with the app in the organization. All time values are UNIX time values.",
        )
        get_developer_by_app.add_argument(
            "--app-name", help="the app name", required=True
        )
        get_developer_by_app.set_defaults(
            func=lambda args: console.log(
                Developers(args, args.org, None)
                .get_developer_by_app(args.app_name)
                .text
            )
        )

    def _build_list_developers_argument(self):
        list_developers = self._parser_developers.add_parser(
            "list",
            aliases=["list-developers"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._prefix_parser(),
            ],
            help="Lists all developers in an organization by email address. This call does not list any company developers who are a part of the designated organization.",
        )
        list_developers.add_argument(
            "--expand",
            action="store_true",
            help="Set to true to list developers exanded with details.",
        )
        list_developers.add_argument(
            "--count",
            default=1000,
            type=int,
            help="Limits the list to the number you specify. Use with the startKey parameter to provide more targeted filtering. The limit is 1000.",
        )
        list_developers.add_argument(
            "--startkey",
            default="",
            help="To filter the keys that are returned, enter the email of a developer that the list will start with.",
        )
        list_developers.set_defaults(
            func=lambda args: console.log(
                Developers(args, args.org, None).list_developers(
                    prefix=args.prefix,
                    expand=args.expand,
                    count=args.count,
                    startkey=args.startkey,
                )
            )
        )

    def _build_set_developer_status_argument(self):
        set_developer_status = self._parser_developers.add_parser(
            "set-status",
            aliases=["set-developer-status"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._prefix_parser(),
            ],
            help="Sets a developer's status to active or inactive for a specific organization. Run this API for each organization where you want to change the developer's status.",
        )
        set_developer_status.add_argument(
            "-n",
            "--name",
            help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
            required=True,
        )
        set_developer_status.add_argument(
            "--action", choices=("active", "inactive"), type=str, help="", required=True
        )
        set_developer_status.set_defaults(
            func=lambda args: console.log(
                Developers(args, args.org, args.name)
                .set_developer_status(args.action)
                .text
            )
        )

    def _build_update_developer_argument(self):
        set_developer_status = self._parser_developers.add_parser(
            "update",
            aliases=["update-developer"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
                self._prefix_parser(),
            ],
            help="Update an existing developer profile. To add new values or update existing values, submit the new or updated portion of the developer profile along with the rest of the developer profile, even if no values are changing. To delete attributes from a developer profile, submit the entire profile without the attributes that you want to delete.",
        )
        set_developer_status.add_argument(
            "-n",
            "--name",
            help="The developer's email. This value is used to uniquely identify the developer in Apigee Edge.",
            required=True,
        )
        set_developer_status.add_argument(
            "-b", "--body", help="request body", required=True
        )
        set_developer_status.set_defaults(
            func=lambda args: console.log(
                Developers(args, args.org, args.name).update_developer(args.body).text
            )
        )

    def _build_update_a_developer_attribute_argument(self):
        update_a_developer_attribute = self._parser_developers.add_parser(
            "update-attr",
            aliases=["update-attribute", "update-a-developer-attribute"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
            help="Updates the value of a developer attribute.",
        )
        update_a_developer_attribute.add_argument(
            "-n", "--name", help="the developer's email address", required=True
        )
        update_a_developer_attribute.add_argument(
            "--attribute-name", help="attribute name", required=True
        )
        update_a_developer_attribute.add_argument(
            "--updated-value", help="updated value", required=True
        )
        update_a_developer_attribute.set_defaults(
            func=lambda args: console.log(
                Developers(args, args.org, args.name)
                .update_a_developer_attribute(args.attribute_name, args.updated_value)
                .text
            )
        )

    def _build_delete_developer_attribute_argument(self):
        delete_developer_attribute = self._parser_developers.add_parser(
            "delete-attr",
            aliases=["delete-attribute", "delete-developer-attribute"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
            help="Deletes a developer attribute.",
        )
        delete_developer_attribute.add_argument(
            "-n", "--name", help="the developer's email address", required=True
        )
        delete_developer_attribute.add_argument(
            "--attribute-name", help="attribute name", required=True
        )
        delete_developer_attribute.set_defaults(
            func=lambda args: console.log(
                Developers(args, args.org, args.name)
                .delete_developer_attribute(args.attribute_name)
                .text
            )
        )

    def _build_get_all_developer_attributes_argument(self):
        get_all_developer_attributes = self._parser_developers.add_parser(
            "get-attrs",
            aliases=["get-attributes", "get-all-developer-attributes"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
            help="Returns a list of all developer attributes.",
        )
        get_all_developer_attributes.add_argument(
            "-n", "--name", help="the developer's email address", required=True
        )
        get_all_developer_attributes.set_defaults(
            func=lambda args: console.log(
                Developers(args, args.org, args.name)
                .get_all_developer_attributes()
                .text
            )
        )

    def _build_update_all_developer_attributes_argument(self):
        update_all_developer_attributes = self._parser_developers.add_parser(
            "update-all-attrs",
            aliases=["update-all-attributes", "update-all-developer-attributes"],
            parents=[
                self._parent_parser(),
                self._silent_parser(),
                self._verbose_parser(),
            ],
            help="Updates or creates developer attributes. This API replaces the current list of attributes with the attributes specified in the request body. This lets you update existing attributes, add new attributes, or delete existing attributes by omitting them from the request body.",
        )
        update_all_developer_attributes.add_argument(
            "-n", "--name", help="the developer's email address", required=True
        )
        update_all_developer_attributes.add_argument(
            "-b", "--body", help="request body", required=True
        )
        update_all_developer_attributes.set_defaults(
            func=lambda args: console.log(
                Developers(args, args.org, args.name)
                .update_all_developer_attributes(args.body)
                .text
            )
        )

    def _create_parser(self):
        self._build_create_developer_argument()
        self._build_delete_developer_argument()
        self._build_get_developer_argument()
        self._build_get_developer_by_app_argument()
        self._build_list_developers_argument()
        self._build_set_developer_status_argument()
        self._build_update_developer_argument()
        self._build_update_a_developer_attribute_argument()
        self._build_delete_developer_attribute_argument()
        self._build_get_all_developer_attributes_argument()
        self._build_update_all_developer_attributes_argument()
