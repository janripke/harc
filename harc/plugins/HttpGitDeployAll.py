import json
from harc.plugins.Plugable import Plugable
from requests import post
from harc.plugins.PluginException import PluginException
from harc.system.Settings import Settings


class HttpGitDeployAll(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def execute(arguments, settings, properties):

        version = arguments.v
        environment = arguments.e
        server_username = arguments.u
        server_password = arguments.p

        if not version:
            raise PluginException("no version")

        if not server_username:
            raise PluginException("no username")

        if not server_password:
            raise PluginException("no password")

        if not environment:
            environment = "dev"
            print "using environment : " + environment

        projects = settings['projects']

        for project in projects:

            detail = Settings.find_detail(settings, project['name'], environment)

            if not detail:
                message = "detail for project " + project['name'] + ' and environment ' + environment + " not found"
                raise PluginException(message)

            server = detail['server']

            message = {"username": server_username, "password": server_password}
            headers = {'Content-Type': 'application/json'}
            response = post(server + '/login', json.dumps(message), headers=headers)
            status_code = response.status_code
            if status_code != 200:
                message = "status_code: " + str(response.status_code) + " reason: " + response.reason
                raise PluginException(message)

            content = json.loads(response.content)
            session = content['session']

            message = {"command": "git:deploy", "session": session, "-v": version, "-e": environment, "-n": project['name']}
            headers = {'Content-Type': 'application/json'}
            response = post(server + '/job', json.dumps(message), headers=headers)
            status_code = response.status_code
            if status_code != 200:
                message = "status_code: " + response.status_code + " reason: " + response.reason
                raise PluginException(message)
            print "project: " + project['name'] + ", job_name: " + str(json.loads(response.content)['job_name'])
