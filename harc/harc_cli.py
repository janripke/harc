#!/usr/bin/env python

import os
from os.path import expanduser
from harc.plugins.plugin_command import PluginCommand
from harc.system import utils

import harc
import click


@click.command(cls=PluginCommand, invoke_without_command=True, no_args_is_help=True)
@click.option('-r', '--revision', is_flag=True, help="Report the version of Quark and exit.")
@click.option('-b', '--bypass', is_flag=True, help="Bypass the local configurations.")
@click.pass_context
def main(ctx, revision, bypass):

    # initialize the logger
    utils.load_logger('log.json', 'harc')

    # is there a harc.json
    if not os.path.isfile("harc.json"):
        raise FileNotFoundError("File 'harc.json' not found.")

    # Read the project settings
    properties = utils.load_json('harc.json')
    properties['current.dir'] = os.path.abspath('.')
    properties['module.dir'] = os.path.dirname(harc.__file__)
    properties['home.dir'] = expanduser('~')
    properties['plugin.dir'] = os.path.join(properties.get('module.dir'), 'plugins')

    if not bypass:
        config = utils.load_json('config.json')
        if config:
            properties.update(config)

    ctx.obj = properties

    # show the revision
    if revision:
        print(harc.__title__ + " version " + harc.__version__)
        ctx.exit()


if __name__ == '__main__':
    main()
