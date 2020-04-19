import argparse
import os


class ArgumentType:
    @staticmethod
    def isfile(f):
        if os.path.isfile(f):
            return f
        raise argparse.ArgumentTypeError("not a file")

    @staticmethod
    def isdir(d):
        if os.path.isdir(d):
            return d
        raise argparse.ArgumentTypeError("not a directory")

    @staticmethod
    def ispath(f):
        if os.path.exists(f):
            return f
        raise argparse.ArgumentTypeError("not a valid path")


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
