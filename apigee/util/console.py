import builtins
import sys

import apigee


def log(*message, status=None, silent=False, curr_verbosity=0, expc_verbosity=0):
    toggle_silent = False
    toggle_verbose = 0
    try:  # hack
        toggle_silent = builtins.APIGEE_CLI_TOGGLE_SILENT
        toggle_verbose = builtins.APIGEE_CLI_TOGGLE_VERBOSE
    except AttributeError:
        pass
    if silent or toggle_silent:
        if status:
            sys.exit(status)
        return
    if curr_verbosity or toggle_verbose >= expc_verbosity:
        print(*message)
    if status:
        sys.exit(status)
