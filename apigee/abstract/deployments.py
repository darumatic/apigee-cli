#!/usr/bin/env python
"""https://apidocs.apigee.com/api/deployments"""

from abc import ABC, abstractmethod

class IDeployments:

    def __init__(self, args, format=False):
        self._args = args
        self._format = format

    def __call__(self):
        pass

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value

    @abstractmethod
    def get_api_proxy_deployment_details(self):
        pass
