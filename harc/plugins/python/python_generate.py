import uuid
import os
import logging
from urllib.parse import urlparse, quote

import click

from harc.system.Git import Git
from harc.system.System import System
from harc.system.Docker import Docker
from harc.system.io.File import File
from harc.system.Requirements import Requirements
from harc.system.PropertyHelper import PropertyHelper

from harc.plugins.UsernameOption import UsernameOption
from harc.plugins.PasswordOption import PasswordOption
from harc.plugins.EnvironmentOption import EnvironmentOption

from harc.shell.key import Key


class DPythonGenerate:
    @click.command()
    # @click.option('-u', '--username', cls=UsernameOption, required=True)
    # @click.option('-p', '--password', cls=PasswordOption, required=True, hide_input=True)
    # @click.option('-v', '--version', required=False, default='master')
    # @click.option('-e', '--environment', cls=EnvironmentOption, required=True)
    @click.pass_context
    def execute(ctx, username, password, version, environment):
        logger = logging.getLogger()
        # logger.debug("username : {}, version: {}, environment : {}".format(username, version, environment))

        # retrieve the properties, set by the cli
        properties = ctx.obj

