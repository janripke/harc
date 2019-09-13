from harc.shell.command import Command
from harc.shell.parameter import Parameter


class AzKeyVault(object):

    @staticmethod
    def list(subscription=None, resource_group=None):
        statement = "az keyvault list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def find(name, subscription=None, resource_group=None):
        vaults = AzKeyVault.list(subscription, resource_group)
        for vault in vaults:
            if vault['name'] == name:
                return vault

    @staticmethod
    def exists(name, subscription=None, resource_group=None):
        if AzKeyVault.find(name, subscription, resource_group):
            return True
        return False

    @staticmethod
    def set_policy(name, resource_group, object_id, secret_permissions=None, env=None):
        statement = "az keyvault set-policy {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--resource-group', resource_group),
            Parameter.format('--object-id', object_id),
            Parameter.format('--secret-permissions', secret_permissions)
        )
        output = Command.execute(statement, env=env)
        return Command.jsonify(output)