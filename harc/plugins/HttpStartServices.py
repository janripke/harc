import json
from harc.plugins.Plugable import Plugable
from requests import post
from harc.plugins.PluginException import PluginException
from harc.system.Settings import Settings


class HttpStartServices(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def execute(arguments, settings, properties):
        server_username = arguments.u
        server_password = arguments.p
        environment = arguments.e

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
            server = detail['server']

            if not detail:
                message = "detail for project " + project['name'] + ' and environment ' + environment + " not found"
                raise PluginException(message)

            services = detail['services']

            message = {"username": server_username, "password": server_password}
            headers = {'Content-Type': 'application/json'}
            response = post(server + '/login', json.dumps(message), headers=headers)
            status_code = response.status_code
            if status_code != 200:
                message = "status_code: " + str(response.status_code) + " reason: " + response.reason + ", content: " + response.content
                raise PluginException(message)

            content = json.loads(response.content)
            session = content['session']

            for service in services:

                message = {"command": "service:start", "session": session, "-s": service['name'], "-e": environment, "-n": project['name']}
                headers = {'Content-Type': 'application/json'}
                response = post(server + '/job', json.dumps(message), headers=headers)
                status_code = response.status_code
                if status_code != 200:
                    message = "service: " + service['name'] + ", status_code: " + str(response.status_code) + ", reason: " + response.reason + ", content: " + response.content
                    raise PluginException(message)
                print "service: " + service['name'] + ", job_name: " + str(json.loads(response.content)['job_name'])
