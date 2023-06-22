import builtins
import sys


def echo(
    *message,
    exit_status=None,
    make_silent=False,
    current_verbosity=0,
    expected_verbosity=0,
    line_ending="\n",
    should_flush=False
):
    toggle_silent = builtins.APIGEE_CLI_TOGGLE_SILENT
    toggle_verbose = builtins.APIGEE_CLI_TOGGLE_VERBOSE
    if make_silent or toggle_silent:
        if exit_status:
            sys.exit(exit_status)
        return
    if current_verbosity or toggle_verbose >= expected_verbosity:
        print(*message, end=line_ending, flush=should_flush)
    if exit_status:
        sys.exit(exit_status)
