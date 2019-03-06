from subprocess import Popen, PIPE
from harc.plugins.PluginException import PluginException


class Twine(object):
    def __init(self):
        object.__init__(self)

    @staticmethod
    def upload(folder):
        statement = "twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose"
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output

    @staticmethod
    def setup():
        statement = "python3 setup.py bdist_wheel"
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output