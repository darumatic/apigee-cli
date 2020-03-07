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
