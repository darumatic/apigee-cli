import os
import re
import sys
# read the contents of your README file
from os import path

from apigee import APP
from apigee import __version__ as version
from apigee import description

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

SETUP_ARGS = dict(
    name=APP,
    version=version,
    description=(description),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/darumatic/apigee-cli",
    author="Matthew Delotavo",
    author_email="matthew.t.delotavo@gmail.com",
    license="Apache license 2.0",
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
    ],
    # py_modules = ['apigee',],
    # entry_points='''
    #     [console_scripts]
    #     apigee=apigee.__main__:main
    # ''',
    entry_points={"console_scripts": ["apigee=apigee.__main__:main"]},
    install_requires=[
        "click==8.1.3",
        "click-aliases==1.0.1",
        "click-option-group==0.5.5",
        "colorama==0.4.6",
        "coverage==7.0.1",
        "GitPython==3.1.30",
        "pudb==2022.1.3",
        "PyJWT==2.6.0",
        "pyotp==2.8.0",
        "python-gnupg>=0.3.5,<0.5.0",  # Note the updated version range
        "requests==2.28.1",
        "tabulate==0.9.0",
        "tqdm==4.64.1",
    ],
    project_urls={"Documentation": "https://darumatic.github.io/apigee-cli/index.html"},
    python_requires=">=3.7",
)

if __name__ == "__main__":
    from setuptools import setup, find_packages

    SETUP_ARGS["packages"] = find_packages()
    setup(**SETUP_ARGS)
