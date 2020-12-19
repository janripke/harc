from subprocess import Popen, PIPE
from harc.system.exceptions import PluginException


def upload(folder):
    statement = "twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose"
    p = Popen([statement], stdout=PIPE, shell=True)
    output, error = p.communicate()
    if p.returncode != 0:
        raise PluginException(error)
    return output


def setup():
    statement = "python3 load.py bdist_wheel"
    p = Popen([statement], stdout=PIPE, shell=True)
    output, error = p.communicate()
    if p.returncode != 0:
        raise PluginException(error)
    return output



