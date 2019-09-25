import argparse
import builtins


class SilentParser:
    def __init__(self):
        self._parent_parser = argparse.ArgumentParser(add_help=False)
        self._build_silent_argument()
        self._silent = self._parent_parser.parse_known_args()[0].silent
        builtins.APIGEE_CLI_TOGGLE_SILENT = self._silent
        self._create_parser()

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    def __call__(self):
        return self._parent_parser

    def _build_silent_argument(self):
        self._parent_parser.add_argument(
            # "-s",
            "--silent",
            action="store_true",
            help="toggle silent output",
            required=False,
        )

    def _create_parser(self):
        pass
