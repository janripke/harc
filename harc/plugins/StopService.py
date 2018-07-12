from harc.plugins.Plugable import Plugable
from harc.plugins.PluginException import PluginException
from harc.system.Systemctl import Systemctl
from harc.system.logger.Logger import Logger
from harc.system.Traceback import Traceback


class StopService(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def execute(arguments, settings, properties):
        job_name = properties['job_name']
        logger = Logger(StopService())
        try:
            s = arguments.s
            environment = arguments.e
            project = arguments.n

            if not s:
                raise PluginException("no service")

            if not environment:
                raise PluginException("no environment")

            if not project:
                raise PluginException("no project")

            details = settings[environment]
            for detail in details:
                if detail['name'] == project:
                    services = detail['services']
                    for service in services:
                        if service['name'] == s:
                            service_password = service['password']
                            result = Systemctl.stop(s, service_password)
                            logger.info(job_name, str(result))
        except:
            result = Traceback.build()
            logger.fatal(job_name, result['message'], result['backtrace'])

