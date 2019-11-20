#!/usr/bin/env python
"""https://apidocs.apigee.com/api/deployments"""

from abc import ABC, abstractmethod

class IDeployments:

    def __init__(self, args, isformat=False):
        self._args = args
        self._isformat = isformat

    def __call__(self):
        pass

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @property
    def isformat(self):
        return self._isformat

    @isformat.setter
    def isformat(self, value):
        self._isformat = value

    @abstractmethod
    def get_api_proxy_deployment_details(self):
        pass
