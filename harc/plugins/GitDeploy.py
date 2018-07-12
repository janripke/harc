from harc.plugins.Plugable import Plugable
from harc.plugins.PluginException import PluginException
from harc.system.Git import Git
from harc.system.System import System
from harc.system.Package import Package
from harc.system.logger.Logger import Logger
from harc.system.Traceback import Traceback
from harc.system.Settings import Settings
from harc.system.Pip import Pip
import urllib


class GitDeploy(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def execute(arguments, settings, properties):
        job_name = properties['job_name']
        logger = Logger(GitDeploy())
        try:

            version = arguments.v
            environment = arguments.e
            project_name = arguments.n

            if not version:
                raise PluginException("no version")

            if not project_name:
                raise PluginException("no project")

            # if no environment is given, dev is assumed.
            if not environment:
                environment = "dev"
                logger.info(job_name, "using environment : " + environment)

            project = Settings.find_project(settings, project_name)

            if not project:
                message = "project " + project_name + " not found"
                raise PluginException(message)

            details = settings[environment]

            username = project['username']
            password = project['password']
            repository = project['repository'].format(urllib.quote(username), urllib.quote(password))

            for detail in details:
                if detail['name'] == project['name']:
                    virtualenv = detail['virtualenv']
                    result = Pip.install(repository, version, project, virtualenv)
                    logger.info(job_name, str(result))

        except:
            result = Traceback.build()
            logger.fatal(job_name, result['message'], result['backtrace'])


