from subprocess import Popen, PIPE
from harc.plugins.PluginException import PluginException


class Package(object):
    def __init(self):
        object.__init__(self)

    @staticmethod
    def install(folder, virtualenv):
        statement = "cd " + folder + ";" + "source " + virtualenv + "/bin/activate ;" + " python load.py install"
        p = Popen([statement], stdout=PIPE, stderr=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output
