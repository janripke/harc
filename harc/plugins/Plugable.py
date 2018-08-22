#!/usr/bin/env python
from harc.plugins.PluginException import PluginException


class Plugable(object):

    def __init__(self):
        object.__init__(self)

    @staticmethod
    def execute(arguments, settings):
        raise PluginException("method not implemented")
