from setuptools import setup, find_packages

from apigee import APP, __version__, description

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=APP,
    version=__version__,
    description=description,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Matthew Delotavo",
    author_email="matthew.t.delotavo@gmail.com",
    url="https://github.com/mdelotavo/apigee-cli",
    download_url=f"https://github.com/mdelotavo/apigee-cli/archive/v{__version__}.tar.gz",
    keywords=["apigee", "management", "api", "oauth", "mfa"],
    packages=find_packages(),
    entry_points={"console_scripts": ["apigee=apigee.__main__:main"]},
    python_requires=">=3.6",
    install_requires=["pyotp", "requests", "tqdm", "tabulate", "pyjwt"],
    license="Apache license 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    project_urls={"Documentation": "https://mdelotavo.github.io/apigee-cli/index.html"},
)
