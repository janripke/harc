from harc.shell.parameter import Parameter
from harc.shell.command import Command
import logging


class AzContainer:

    @staticmethod
    def list(subscription=None, resource_group=None):
        logger = logging.getLogger()
        statement = "az container list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        logger.debug(statement)
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def find(name, subscription=None, resource_group=None):
        containers = AzContainer.list(subscription, resource_group)
        for container in containers:
            if container['name'] == name:
                return container

    @staticmethod
    def exists(name, subscription=None, resource_group=None):
        if AzContainer.find(name, subscription, resource_group):
            return True
        return False

    @staticmethod
    def show(name, resource_group, subscription=None):
        logger = logging.getLogger()
        statement = "az container show {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group)
        )
        logger.debug(statement)
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def create(name, resource_group, image=None, assign_identity=None, cpu=None, memory=None, registry_username=None, registry_password=None, ports=None, dns_name_label=None, command_line=None, env=None):
        logger = logging.getLogger()
        statement = "az container create {} {} {} {} {} {} {} {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--resource-group', resource_group),
            Parameter.format('--image', image),
            Parameter.format('--assign-identity', assign_identity),
            Parameter.format('--cpu', cpu),
            Parameter.format('--memory', memory),
            Parameter.format('--registry-username', registry_username),
            Parameter.format('--registry-password', registry_password),
            Parameter.format('--ports', ports),
            Parameter.format('--dns-name-label', dns_name_label),
            Parameter.format('--command-line', command_line)
        )
        logger.debug(statement)
        output = Command.execute(statement, env=env)
        return Command.jsonify(output)
