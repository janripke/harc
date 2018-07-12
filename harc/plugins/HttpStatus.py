import json
from harc.plugins.Plugable import Plugable
from requests import post
from harc.plugins.PluginException import PluginException
from harc.system.Settings import Settings


class HttpStatus(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def execute(arguments, settings, properties):
        server_username = arguments.u
        server_password = arguments.p
        job_name = arguments.j
        environment = arguments.e

        if not server_username:
            raise PluginException("no username")

        if not server_password:
            raise PluginException("no password")

        if not job_name:
            raise PluginException("no job_name")

        if not environment:
            environment = "dev"
            print "using environment : " + environment

        projects = settings['projects']

        project = projects[0]
        detail = Settings.find_detail(settings, project['name'], environment)
        server = detail['server']

        if not detail:
            message = "detail for project " + project['name'] + ' and environment ' + environment + " not found"
            raise PluginException(message)

        message = {"username": server_username, "password": server_password}
        headers = {'Content-Type': 'application/json'}
        response = post(server + '/login', json.dumps(message), headers=headers)
        status_code = response.status_code
        if status_code != 200:
            message = "status_code: " + str(response.status_code) + ", reason: " + response.reason + ", content: " + response.content
            raise PluginException(message)

        content = json.loads(response.content)
        session = content['session']

        message = {"session": session, "job_name": job_name}
        headers = {'Content-Type': 'application/json'}
        response = post(server + '/status', json.dumps(message), headers=headers)
        content = json.loads(response.content)
        status_code = response.status_code

        if status_code != 200:
            message = "job_name: " + job_name + ", status_code: " + str(response.status_code) + ", reason: " + response.reason + ", content: " + response.content
            raise PluginException(message)

        if content:
            for c in content:
                print c['message']

        if not content:
            print "no info found for job " + job_name
