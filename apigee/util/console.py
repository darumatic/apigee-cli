import sys
def log(*message, status=None):
    print(*message)
    if status:
        sys.exit(status)
