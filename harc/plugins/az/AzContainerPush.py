from harc.plugins.PluginException import PluginException
from harc.azure.AzContainerRegistry import AzContainerRegistry
from harc.system.Docker import Docker
from harc.system.PropertyHelper import PropertyHelper
from harc.plugins.EnvironmentOption import EnvironmentOption
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

        registry_name = registration.get('name')
        logger.debug("registry name : {}".format(registry_name))
        AzContainerRegistry.login(registry_name)

        # tag your image in azure format
        login_server = registration.get('loginServer')
        name = "{}_{}:{}".format(project_name, environment, version)
        result = Docker.tag(name, login_server)
        print(result)

        # push the image to the azure container registry
        result = Docker.push(name, login_server)
        print(result)


