#!/usr/bin/env python
"""https://docs.apigee.com/api-platform/system-administration/permissions"""

from abc import ABC, abstractmethod

class IPermissions:

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
    def create_permissions(self):
        pass

    @abstractmethod
    def team_permissions(self):
        pass

    @abstractmethod
    def get_permissions(self):
        pass
