from subprocess import Popen, PIPE
from harc.plugins.PluginException import PluginException


class Pip:
    def __init__(self):
        pass

    @staticmethod
    def install_virtualenv(virtualenv, repository, version, project_name):
        statement = "source " + virtualenv + "/bin/activate ;" + \
                    "pip install git+" + repository + "#egg=" + project_name + \
                    " --process-dependency-links"

        if version:
            statement = "source " + virtualenv + "/bin/activate ;" + \
                        "pip install git+" + repository + "@" + version + "#egg=" + project_name + \
                        " --process-dependency-links"

        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output

    @staticmethod
    def install(module, target_folder):
        statement = "pip install " + module + " -t " + target_folder
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output

    @staticmethod
    def install_python3(module, target_folder):
        statement = "pip install " + module + " -t " + target_folder
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output