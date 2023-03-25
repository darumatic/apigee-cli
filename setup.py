import os

from setuptools import find_packages, setup

from apigee import APP
from apigee import __version__ as version
from apigee import description

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=APP,
    version=version,
    description=description,
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
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["apigee=apigee.__main__:main"]},
    install_requires=[
        "click",
        "click-aliases",
        "click-option-group",
        "colorama",
        "coverage",
        "gitpython",
        "pudb",
        "pyjwt",
        "pyotp",
        "python-gnupg>=0.3.5",
        "requests",
        "tabulate",
        "tqdm",
    ],
    project_urls={"Documentation": "https://darumatic.github.io/apigee-cli/index.html"},
    python_requires=">=3.8",
    packages=find_packages(),
)
