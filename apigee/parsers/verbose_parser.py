import argparse
import builtins
import http.client as http_client
import logging
import requests


class VerboseParser:
    def __init__(self):
        self._parent_parser = argparse.ArgumentParser(add_help=False)
        self._build_verbose_argument()
        self._verbose = self._parent_parser.parse_known_args()[0].verbose
        builtins.APIGEE_CLI_TOGGLE_VERBOSE = self._verbose
        if self._verbose:
            http_client.HTTPConnection.debuglevel = self._verbose - 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
        self._create_parser()

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    def __call__(self):
        return self._parent_parser

    def _build_verbose_argument(self):
        self._parent_parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            help="toggle verbose output",
            required=False,
            default=0,
        )

    def _create_parser(self):
        pass
