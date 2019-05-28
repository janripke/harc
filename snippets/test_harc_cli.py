#!/usr/bin/env python
import click
import os
import harc
from os.path import expanduser
import json
from harc.system.Profile import Profile
from harc.system.logger.LogConfig import LogConfig
import logging
# todo: hoe properties door te geven.


# @click.command()
# @click.option('-a', '--alias', required=True, default='localhost')
# @click.pass_obj

class UsernameOption(click.Option):

    def get_default(self, ctx):
        properties = ctx.obj
        project_name = properties.get('name')
        username = None
        credentials = Profile.credentials(project_name, properties)
        if credentials:
            username = credentials.get('username')
        self.default = username
        return super(UsernameOption, self).get_default(ctx)


class PasswordOption(click.Option):

    def get_default(self, ctx):
        properties = ctx.obj
        project_name = properties.get('name')
        password = None
        credentials = Profile.credentials(project_name, properties)
        if credentials:
            password = credentials.get('password')
        self.default = password
        return super(PasswordOption, self).get_default(ctx)


class EnvironmentOption(click.Option):
    def get_default(self, ctx):
        properties = ctx.obj
        self.default = properties.get('default_environment')
        return super(EnvironmentOption, self).get_default(ctx)


class PluginCommand(click.MultiCommand):

    def list_commands(self, ctx):
        commands = list()
        commands.append('git:branches')
        commands.append('git:release')
        commands.append('az:container:push')
        return commands

    def get_command(self, ctx, cmd_name):
        if cmd_name == "git:release":
            return GitRelease.execute
        if cmd_name == "git:branches":
            return GitBranches.execute
        if cmd_name == "az:container:push":
            return AzContainerPush.execute


class GitRelease:

    @click.command()
    @click.option('-u', '--username', cls=UsernameOption, required=True)
    @click.option('-p', '--password', cls=PasswordOption, required=True)
    @click.option('-b', '--branche', required=False)
    @click.option('-v', '--version', required=False)
    def execute(username, password, branche, version):
        logger = logging.getLogger()
        logger.info("username :{}, password :{}, branche :{}, version: {}".format(username, password, branche, version))


class GitBranches:

    @click.command()
    @click.option('-u', '--username', cls=UsernameOption, required=True)
    @click.option('-p', '--password', cls=PasswordOption, required=True)
    @click.pass_context
    def execute(ctx, username, password):
        logger = logging.getLogger()
        logger.info("username :{}, password :{}".format(username, password))


class AzContainerPush:

    @click.command()
    @click.option('-u', '--username', cls=UsernameOption, required=True)
    @click.option('-p', '--password', cls=PasswordOption, required=True)
    @click.option('-v', '--version', required=True, prompt='release version')
    @click.option('-e', '--environment', cls=EnvironmentOption, required=True)
    def execute(username, password, version, environment):
        print('az_container_push, username:', username)
        print('az_container_push, password:', password)
        print('az_container_push, version:', version)
        print('az_container_push, environment:', environment)


@click.command(cls=PluginCommand, invoke_without_command=True, no_args_is_help=True)
@click.option('-r', '--revision', is_flag=True, help="Report the version of Harc and exit.")
@click.pass_context
def main(ctx, revision):

    # Read the project settings
    f = open("harc.json")
    properties = json.load(f)

    properties['current.dir'] = os.path.abspath('.')
    properties['harc.dir'] = os.path.dirname(harc.__file__)
    properties['home.dir'] = expanduser('~')
    properties['plugin.dir'] = os.path.join(properties.get('harc.dir'), 'plugins')

    ctx.obj = properties

    # initialize the logger
    LogConfig.load('log.json', 'harc')

    # show the revision
    if revision:
        print(harc.__title__ + " version " + harc.__version__)
        ctx.exit()

# properties laden en doorgeven, kan via ctx.obj
# username end password op basis van project in properties
# python click default value using context




# cli = PluginCommand(help='This tool\'s subcommands are loaded from a plugin folder dynamically.')

if __name__ == '__main__':
    main()

