import os
import re
import sys
# read the contents of your README file
from os import path

from apigee import APP
from apigee import __version__ as version
from apigee import description

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

SETUP_ARGS = dict(
    name=APP,
    version=version,
    description=(description),
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/mdelotavo/apigee-cli',
    author='Matthew Delotavo',
    author_email='matthew.t.delotavo@gmail.com',
    license='Apache license 2.0',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    # py_modules = ['apigee',],
    # entry_points='''
    #     [console_scripts]
    #     apigee=apigee.__main__:main
    # ''',
    entry_points={'console_scripts': ['apigee=apigee.__main__:main']},
    install_requires=[
        'requests>=2.22',
        'click',
        'click-aliases',
        'click-option-group',
        'colorama',
        'pyotp',
        'requests',
        'tqdm',
        'tabulate',
        'pyjwt',
        'python-gnupg>=0.3.5',
    ],
    project_urls={'Documentation': 'https://mdelotavo.github.io/apigee-cli/index.html'},
    python_requires='>=3.6',
)

if __name__ == '__main__':
    from setuptools import setup, find_packages

    SETUP_ARGS['packages'] = find_packages()
    setup(**SETUP_ARGS)
