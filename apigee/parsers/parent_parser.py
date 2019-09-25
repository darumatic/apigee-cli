import argparse

from apigee import APIGEE_ORG
from apigee import APIGEE_USERNAME
from apigee import APIGEE_PASSWORD
from apigee import APIGEE_MFA_SECRET
from apigee.util import *


class ParentParser:
    def __init__(self):
        self._parent_parser = argparse.ArgumentParser(add_help=False)
        self._build_profile_argument()
        self._profile = self._parent_parser.parse_known_args()[0].profile
        self._create_parser()

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, value):
        self._profile = value

    def __call__(self):
        return self._parent_parser

    def _build_profile_argument(self):
        self._parent_parser.add_argument(
            "-P",
            "--profile",
            action="store",
            help="name of credentials profile",
            default="default",
        )

    def _build_mfa_secret_argument(self):
        mfa_secret = authorization.get_credential(self._profile, "mfa_secret")
        self._parent_parser.add_argument(
            "--mfa-secret",
            action="store",
            help="apigee mfa secret",
            required=False,
            default=APIGEE_MFA_SECRET if mfa_secret is None else mfa_secret,
        )

    def _build_org_argument(self):
        org = authorization.get_credential(self._profile, "org")
        if org:
            self._parent_parser.add_argument(
                "-o",
                "--org",
                action="store",
                help="apigee org",
                required=False,
                default=org,
            )
        elif APIGEE_ORG:
            self._parent_parser.add_argument(
                "-o",
                "--org",
                action="store",
                help="apigee org",
                required=False,
                default=APIGEE_ORG,
            )
        else:
            self._parent_parser.add_argument(
                "-o", "--org", action="store", help="apigee org", required=True
            )

    def _build_username_argument(self):
        username = authorization.get_credential(self._profile, "username")
        if username:
            self._parent_parser.add_argument(
                "-u",
                "--username",
                action="store",
                help="apigee username",
                required=False,
                default=username,
            )
        elif APIGEE_USERNAME:
            self._parent_parser.add_argument(
                "-u",
                "--username",
                action="store",
                help="apigee username",
                required=False,
                default=APIGEE_USERNAME,
            )
        else:
            self._parent_parser.add_argument(
                "-u",
                "--username",
                action="store",
                help="apigee username",
                required=True,
            )

    def _build_password_argument(self):
        password = authorization.get_credential(self._profile, "password")
        if password:
            self._parent_parser.add_argument(
                "-p",
                "--password",
                action="store",
                help="apigee password",
                required=False,
                default=password,
            )
        elif APIGEE_PASSWORD:
            self._parent_parser.add_argument(
                "-p",
                "--password",
                action="store",
                help="apigee password",
                required=False,
                default=APIGEE_PASSWORD,
            )
        else:
            self._parent_parser.add_argument(
                "-p",
                "--password",
                action="store",
                help="apigee password",
                required=True,
            )

    def _create_parser(self):
        self._build_mfa_secret_argument()
        self._build_org_argument()
        self._build_username_argument()
        self._build_password_argument()
