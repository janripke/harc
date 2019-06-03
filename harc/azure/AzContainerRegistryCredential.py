from harc.shell.Parameter import Parameter
from harc.shell.Command import Command


class AzContainerRegistryCredential:
    @staticmethod
    def show(name, resource_group=None, subscription=None):
        statement = "az acr credential show {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)
