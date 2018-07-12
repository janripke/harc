from subprocess import Popen, PIPE
from harc.plugins.PluginException import PluginException


class Systemctl(object):
    def __init(self):
        object.__init__(self)

    @staticmethod
    def start(service, password):
        statement = "echo " + password + " | " + "sudo -kS systemctl start " + service
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output

    @staticmethod
    def stop(service, password):
        statement = "echo " + password + " | " + "sudo -kS systemctl stop " + service
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output


