import builtins
import sys

import apigee


def log(*message, status=None, silent=False, curr_verbosity=0, expc_verbosity=0):
    try:
        hasattr(builtins, "APIGEE_CLI_TOGGLE_SILENT")
        hasattr(builtins, "APIGEE_CLI_TOGGLE_VERBOSE")
    except AttributeError:
        builtins.APIGEE_CLI_TOGGLE_SILENT = False
        builtins.APIGEE_CLI_TOGGLE_VERBOSE = 0
    if silent or builtins.APIGEE_CLI_TOGGLE_SILENT:
        if status:
            sys.exit(status)
        return
    if curr_verbosity or builtins.APIGEE_CLI_TOGGLE_VERBOSE >= expc_verbosity:
        print(*message)
    if status:
        sys.exit(status)
