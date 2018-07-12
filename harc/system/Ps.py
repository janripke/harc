import psutil
from subprocess import Popen, PIPE
from harc.plugins.PluginException import PluginException


class Ps:
    def __init__(self):
        pass

    @staticmethod
    def is_active(process_name):
        for proc in psutil.process_iter():
            if proc.name() == process_name:
                return True
        return False

    @staticmethod
    def kill(process_name):
        for proc in psutil.process_iter():
            if proc.name() == process_name:
                proc.kill()

    @staticmethod
    def start(virtualenv, daemon_name):
        statement = "source " + virtualenv + "/bin/activate;" + \
                    daemon_name + "&"

        print statement
        p = Popen([statement], stdout=PIPE)
        # pid = Popen([statement]).pid
        # return pid
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output

        # pid = Popen(["/bin/mycmd", "myarg"]).pid