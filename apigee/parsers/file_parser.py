import argparse

from apigee.util.types import ArgumentType


class FileParser:
    def __init__(self):
        self._parent_parser = argparse.ArgumentParser(add_help=False)
        self._create_parser()

    @property
    def parent_parser(self):
        return self._parent_parser

    @parent_parser.setter
    def parent_parser(self, value):
        self._parent_parser = value

    def __call__(self):
        return self._parent_parser

    def _build_file_argument(self):
        self._parent_parser.add_argument(
            "-f",
            "--file",
            action="store",
            help="file path",
            required=True,
            type=ArgumentType.isfile,
        )

    def _create_parser(self):
        self._build_file_argument()
