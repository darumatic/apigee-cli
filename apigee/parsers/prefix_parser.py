import argparse

from apigee import APIGEE_CLI_PREFIX
from apigee.util import authorization

class PrefixParser:

    def __init__(self, **kwargs):
        self._parent_parser = argparse.ArgumentParser(add_help=False)
        # self._build_profile_argument()
        # self._profile = self._parent_parser.parse_known_args()[0].profile
        self._profile = kwargs.get('profile', 'default')
        self._prefix = authorization.get_credential(self._profile, 'prefix')
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

    # def _build_profile_argument(self):
    #     self._parent_parser.add_argument('-P', '--profile', action='store', help='name of credentials profile', default='default')

    def _build_prefix_argument(self):
        self._parent_parser.add_argument('--prefix', help='prefix filter for apigee items', default=APIGEE_CLI_PREFIX if self._prefix is None else self._prefix)

    def _create_parser(self):
        self._build_prefix_argument()
