import sys
def log(*message, status=0):
    print(*message)
    sys.exit(status)
