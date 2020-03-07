import argparse

from apigee.util.types import ArgumentType


class DirParser:
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

    def _build_directory_argument(self):
        self._parent_parser.add_argument(
            "-d",
            "--directory",
            action="store",
            help="directory path",
            required=True,
            type=ArgumentType.isdir,
        )

    def _create_parser(self):
        self._build_directory_argument()
