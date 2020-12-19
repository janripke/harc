from harc.shell.parameter import Parameter
from harc.shell.command import Command


class AzIdentity(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(resource_group=None, subscription=None, env=None):
        statement = "az identity list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement, env=env)
        return Command.jsonify(output)

    @staticmethod
    def find(name, resource_group=None, subscription=None, env=None):
        identities = AzIdentity.list(resource_group, subscription, env=env)
        for identity in identities:
            if identity['name'] == name:
                return identity

    @staticmethod
    def exists(name, resource_group=None, subscription=None, env=None):
        if AzIdentity.find(name, resource_group=resource_group, subscription=subscription, env=env):
            return True
        return False

    @staticmethod
    def create(name, resource_group, subscription=None, location='westeurope', env=None):
        statement = "az identity create {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--resource-group', resource_group),
            Parameter.format('--subscription', subscription),
            Parameter.format('--location', location),
        )
        output = Command.execute(statement, env=env)
        return Command.jsonify(output)

    @staticmethod
    def delete(name, resource_group=None, subscription=None, env=None):
        statement = "az identity delete {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement, env=env)
        return Command.jsonify(output)