from harc.shell.Parameter import Parameter
from harc.shell.Key import Key
from harc.shell.Command import Command


class Docker:
    @staticmethod
    def build(name, folder, version, proxy=None):
        statement = "docker build {} {} {}".format(
            Parameter.format('--build-arg', proxy),
            Parameter.format('-t', name + ":" + version),
            Parameter.format('', folder)
        )
        output = Command.execute(statement)
        return Command.stringify(output)
        # docker build --build-arg https_proxy=http://nl-userproxy-access.net.abnamro.com:8080 -t poc_flask_docker .

    @staticmethod
    def tag(name, login_server, version):
        statement = "docker tag {} {}/{}:{}".format(
            name,
            login_server,
            name,
            version
        )
        output = Command.execute(statement)
        return Command.stringify(output)
        # docker tag aci-tutorial-app <acrLoginServer>/aci-tutorial-app:v1

    @staticmethod
    def push(name, login_server, version):
        statement = "docker push {}/{}:{}".format(
            login_server,
            name,
            version
        )
        output = Command.execute(statement)
        return Command.stringify(output)
        # docker push mycontainerregistry082.azurecr.io/aci-tutorial-app:v1

    @staticmethod
    def pull(name):
        statement = "docker pull {}".format(
            Parameter.format('', name)
        )
        output = Command.execute(statement)
        return output

    @staticmethod
    def run(name, publish=None):
        statement = "docker run -d {} {}".format(
            Parameter.format('--publish', publish),
            Parameter.format('', name)
        )
        output = Command.execute(statement)
        return Command.stringify(output)

    @staticmethod
    def stop(container_id):
        statement = "docker stop {}".format(
            Parameter.format('', container_id)
        )
        output = Command.execute(statement)
        return Command.stringify(output)

    @staticmethod
    def find(container_id):
        statement = "docker container ls --quiet --filter {}".format(
            Key.format('id', container_id)
        )
        output = Command.execute(statement)
        return Command.stringify(output)

    @staticmethod
    def exists(container_id):
        if Docker.find(container_id):
            return True
        return False