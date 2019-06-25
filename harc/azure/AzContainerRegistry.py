from harc.shell.Parameter import Parameter
from harc.shell.Command import Command


class AzContainerRegistry(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(subscription=None, resource_group=None):
        statement = "az acr list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def find(name, subscription=None, resource_group=None):
        registrations = AzContainerRegistry.list(subscription, resource_group)
        for registration in registrations:
            if registration['name'] == name:
                return registration

    @staticmethod
    def find_by_resource_group(resource_group):
        registrations = AzContainerRegistry.list(resource_group=resource_group)
        if registrations:
            # retrieve the first containter registration.
            # it is assumed that in a resource_group there is only one container registry
            return registrations[0]


    @staticmethod
    def exists(name, subscription=None, resource_group=None):
        if AzContainerRegistry.find(name, subscription, resource_group):
            return True
        return False

    @staticmethod
    def create(name, resource_group, sku, location=None, subscription=None):
        statement = "az acr create {} {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--sku', sku),
            Parameter.format('--location', location),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def delete(name, resource_group, subscription=None):
        statement = "az acr delete {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def login(name):
        statement = "az acr login {}".format(
            Parameter.format('--name', name)
            )
        output = Command.execute(statement)
        return Command.stringify(output)
