from harc.plugins.Plugin import Plugin
from harc.plugins.PluginException import PluginException
from harc.azure.AzContainerRegistry import AzContainerRegistry
from harc.system.Git import Git
from harc.system.System import System
from harc.system.Profile import Profile
from harc.system.Docker import Docker
from harc.system.PropertyHelper import PropertyHelper
from harc.plugins.EnvironmentOption import EnvironmentOption
from urllib.parse import urlparse, quote
from harc.shell.Key import Key
import uuid
import os
import click
import logging


class AzContainerPush:
    @click.command()
    @click.option('-v', '--version', required=True, prompt='release version')
    @click.option('-e', '--environment', cls=EnvironmentOption, required=True)
    @click.pass_context
    def execute(ctx, version, environment):

        logger = logging.getLogger()
        logger.debug("version: {}, environment : {}".format(version, environment))

        # retrieve the properties, set by the cli
        properties = ctx.obj

        project_name = properties['name']
        resource_group = PropertyHelper.find_resource_group(properties, environment)

        # retrieve container registry of this resource_group, reflecting the environment.
        registration = AzContainerRegistry.find_by_resource_group(resource_group=resource_group)

        if not registration:
            raise PluginException("registration not found")

        # tag your image in azure format
        login_server = registration.get('loginServer')
        name = "{}_{}:{}".format(project_name, environment, version)
        result = Docker.tag(name, login_server)
        print(result)

        # push the image to the azure container registry
        result = Docker.push(name, login_server)
        print(result)


