#!/usr/bin/env python

import json
import os
from os.path import expanduser
from harc.system.logger.LogConfig import LogConfig
from harc.plugins.PluginCommand import PluginCommand
from harc.system.config import Config

import harc
import click


def find_file(path, default):
    if os.path.isfile(path):
        return path
    return default


@click.command(cls=PluginCommand, invoke_without_command=True, no_args_is_help=True)
@click.option('-r', '--revision', is_flag=True, help="Report the version of Harc and exit.")
@click.pass_context
def main(ctx, revision):

    # find the log configuration file
    log_file = find_file('log.json', os.path.join(os.path.dirname(harc.__file__), 'log.json'))

    # initialize the logger
    LogConfig.load(log_file, 'harc')

    # is there a harc.json
    if not os.path.isfile("harc.json"):
        raise RuntimeError("harc.json not found.")

    # Read the project settings
    f = open("harc.json")
    properties = json.load(f)
    f.close()

    properties['current.dir'] = os.path.abspath('.')
    properties['module.dir'] = os.path.dirname(harc.__file__)
    properties['home.dir'] = expanduser('~')
    properties['plugin.dir'] = os.path.join(properties.get('module.dir'), 'plugins')

    config = Config.load(properties)
    if config:
        properties.update(config)

    ctx.obj = properties

    # show the revision
    if revision:
        print(harc.__title__ + " version " + harc.__version__)
        ctx.exit()


if __name__ == '__main__':
    main()


