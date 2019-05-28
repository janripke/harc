#!/usr/bin/env python
from harc.plugins.PluginException import PluginException


class Plugable:

    def execute(self, arguments, settings, properties):
        raise PluginException("method not implemented")

