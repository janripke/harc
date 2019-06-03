from harc.shell.Parameter import Parameter
from harc.shell.Command import Command
import logging


class AzContainer:
    @staticmethod
    def list(subscription=None, resource_group=None):
        statement = "az container list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def create(name, resource_group, image=None, cpu=None, memory=None, registry_username=None, registry_password=None, ports=None, dns_name_label=None):
        logger = logging.getLogger()
        statement = "az container create {} {} {} {} {} {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--resource-group', resource_group),
            Parameter.format('--image', image),
            Parameter.format('--cpu', cpu),
            Parameter.format('--memory', memory),
            Parameter.format('--registry-username', registry_username),
            Parameter.format('--registry-password', registry_password),
            Parameter.format('--ports', ports),
            Parameter.format('--dns-name-label', dns_name_label),
        )
        logger.debug(statement)
        output = Command.execute(statement)
        return Command.jsonify(output)

