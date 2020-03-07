import argparse


class EnvironmentParser:
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

    def _build_environment_argument(self):
        self._parent_parser.add_argument(
            "-e", "--environment", help="environment", required=True
        )

    def _create_parser(self):
        self._build_environment_argument()
