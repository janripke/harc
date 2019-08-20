from harc.plugins.docker.DockerBuild import DockerBuild
from harc.system.Profile import Profile
from os.path import expanduser
import unittest
import os
import harc
import json
from click.testing import CliRunner


class Ctx:
    obj = None


class TestDockerBuild(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_buid(self):

        properties = dict()
        properties['current.dir'] = os.path.abspath('.')
        properties['module.dir'] = os.path.dirname(harc.__file__)
        properties['home.dir'] = expanduser('~')
        properties['plugin.dir'] = os.path.join(properties.get('module.dir'), 'plugins')

        properties['name'] = "poc_flask_docker"
        properties['repository'] = "https://cbsp-abnamro.visualstudio.com/ClientAnalytics/_git/poc-flask-docker"
        properties['technology'] = "python"
        properties['default_environment'] = 'local'

        # environments = list()
        # environment = dict()
        # environment['name'] = "local"
        # environments.append(environment)
        #
        # environment = dict()
        # environment['name'] = "sandbox"
        # environment['resource_group'] = "sandbox-nl42949-002-rg"
        # environments.append(environment)

        credentials = Profile.credentials('poc_flask_docker', properties)
        print(credentials)

        username = credentials['username']
        password = credentials['password']
        version = "1.0.0"
        environment = 'local'

        f = open('harc.json')
        properties = json.load(f)
        f.close()

        runner = CliRunner()
        result = runner.invoke(DockerBuild.execute, ['--username', username, '--password', password, '--version', '1.0.0'], obj=properties)
        # DockerBuild.execute(username, password, version, environment)
        print(result)


if __name__ == '__main__':
    unittest.main()
