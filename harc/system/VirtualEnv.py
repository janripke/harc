from subprocess import Popen, PIPE
from harc.plugins.PluginException import PluginException


class VirtualEnv(object):
    def __init(self):
        object.__init__(self)

    @staticmethod
    def create(folder):
        statement = 'virtualenv ' + folder
        p = Popen([statement], stdout=PIPE, stderr=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output
