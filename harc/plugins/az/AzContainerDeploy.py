from harc.plugins.PluginException import PluginException
from harc.azure.AzContainerRegistry import AzContainerRegistry
from harc.azure.AzContainerRegistryCredential import AzContainerRegistryCredential
from harc.azure.AzContainer import AzContainer
from harc.plugins.EnvironmentOption import EnvironmentOption
from harc.system.PropertyHelper import PropertyHelper
import click
import logging


# az container create
# --resource-group sandbox-nl42949-002-rg
# --name poc-flask-docker-dev
# --image aabnlclansandboxcontainerregistry.azurecr.io/poc_flask_docker_dev:1.0.6
# --cpu 1
# --memory 1
# --registry-username aabnlclansandboxcontainerregistry
# --registry-password 8h7Uvwk6Fwt4+6WPoRwu4rlbwVFaNZD7
# --ports 80
# --dns-name-label poc-flask-docker-dev

class AzContainerDeploy:
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
        container = PropertyHelper.find_container(properties, environment)

        # retrieve container registry of this resource_group, reflecting the environment.
        registration = AzContainerRegistry.find_by_resource_group(resource_group=resource_group)
        login_server = registration.get('loginServer')
        registry_name = registration['name']
        logger.debug(registration)

        if not registration:
            raise PluginException("registration not found")

        container_name = "{}_{}".format(project_name, environment).replace('_', '-')
        image_name = "{}/{}_{}:{}".format(login_server, project_name, environment, version)
        cpu = container.get('cpu')
        memory = container.get('memory')
        ports = container.get('ports')

        # retrieve the credentials, this could be seen as a work around for the service principal, keystore method
        credentials = AzContainerRegistryCredential.show(registry_name, resource_group)

        registry_username = credentials['username']
        registry_password = credentials['passwords'][0]['value']

        AzContainer.create(container_name, resource_group, image_name, cpu, memory, registry_username, registry_password, ports, container_name)

        # result = Docker.tag(name, login_server)
        # print(result)
        #
        # # push the image to the azure container registry
        # result = Docker.push(name, login_server)
        # print(result)
