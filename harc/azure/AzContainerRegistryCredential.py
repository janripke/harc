from harc.shell.parameter import Parameter
from harc.shell.command import Command


class AzContainerRegistryCredential:
    @staticmethod
    def show(name, resource_group=None, subscription=None, env=None):
        statement = "az acr credential show {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement, env=env)
        return Command.jsonify(output)
