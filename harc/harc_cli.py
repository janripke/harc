#!/usr/bin/env python

import json
import os
from harc.plugins.PluginFactory import PluginFactory
from harc.system.HarcCliArguments import HarcCliArguments
import harc


def main(args=None):
    # harc = hit and release code, probably python.

    # Instantiate the parser
    parser = HarcCliArguments("harc = Hit And Release Code, probably python.")
    args = parser.parse_args(args)

    if not os.path.isfile("harc.json"):
        raise RuntimeError("harc.json not found.")

    # Read the project settings
    f = open("harc.json")
    settings = json.load(f)

    properties = dict()
    properties['current.dir'] = os.path.abspath('.')
    properties['harc.dir'] = os.path.dirname(harc.__file__)

    plugin = PluginFactory.create_plugin(args.command)
    properties['plugin.dir'] = os.path.join(properties.get('harc.dir'), 'plugins')
    plugin.execute(args, settings, properties)


if __name__ == "__main__":
    main(args=None)


