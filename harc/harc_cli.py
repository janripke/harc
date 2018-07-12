#!/usr/bin/env python

import json
import os
from harc.plugins.PluginFactory import PluginFactory
from harc.system.HarcCliArguments import HarcCliArguments
import inspect


def main(args=None):
    # harc = hit and release code, probably python.

    # Instantiate the parser
    parser = HarcCliArguments("harc = Hit And Release Code, probably python.")
    print args
    args = parser.parse_args(args)

    if not os.path.isfile("harc.json"):
        raise "harc.json not found."

    # Read the project settings
    data = open("harc.json")
    settings = json.load(data)

    properties = {}
    properties['harc_dir'] = os.path.abspath('.')

    plugin = PluginFactory.create_plugin(args.command)
    path, filename = os.path.split(inspect.getfile(plugin))
    properties['plugin_dir'] = path
    plugin.execute(args, settings, properties)


if __name__ == "__main__":
    main(args=None)


