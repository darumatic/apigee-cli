#!/usr/bin/env python

import os
from pathlib import Path

def main(fargs, *args, **kwargs):

    files = []

    for filename in Path(fargs.directory).resolve().rglob('*'):
        if not os.path.isdir(str(filename)) and '/.git/' not in str(filename):
            # print(filename)
            files.append(str(filename))

    for file in files:
        with open(file, 'r') as f:
            body = f.read()
            if fargs.resource in body:
                with open(file, 'w') as new_f:
                    new_f.write(body.replace(fargs.resource, fargs.prefix+fargs.resource))
                print('M  ', file)

if __name__ == '__main__':
    main()
