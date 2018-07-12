import uuid
import unittest
import os
from harc.plugins.AwsLambdaDeploy import AwsLambdaDeploy
from harc.system.HarcCliArguments import HarcCliArguments
from harc.system.Git import Git
from harc.system.System import System
from urlparse import urlparse
import urllib


class TestAwsLambdaDeploy(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_deploy(self):
        properties = dict()
        properties['harc_dir'] = os.path.abspath('.')

        project = dict()
        project['name'] = 'mdp_lambda'
        project['technology'] = 'python'
        project['repository'] = 'ssh://git-codecommit.eu-west-1.amazonaws.com/v1/repos/mdp-lambda'

        double = dict()
        double['dependencies'] = ['requests']
        la = dict()
        la['Double.py'] = double

        lambdas = list()
        lambdas.append(la)

        register = dict()
        register['dependencies'] = ['requests']
        la = dict()
        la['Register.py'] = register
        lambdas.append(la)

        project['lambdas'] = lambdas

        find_lambdas = list()
        find_lambdas.append("lambdas")
        project['find_lambdas'] = find_lambdas

        projects = list()
        projects.append(project)

        settings = dict()
        settings['projects'] = projects

        environment = dict()
        environment['aws_profile_name'] = 'elsevier-mdp-dev'
        environment['aws_bucket_name'] = 'elsevier-mdp-dev-source'
        environment['aws_region_name'] = 'eu-west-1'
        settings['dev'] = environment

        # Instantiate the parser
        parser = HarcCliArguments("harc = Hit And Release Code, probably python.")
        args = parser.parse_args(['aws:lambda:deploy'])

        plugin = AwsLambdaDeploy()
        plugin.execute(args, settings, properties)

        # the


if __name__ == '__main__':
    unittest.main()
