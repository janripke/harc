import unittest
import os
from harc.plugins.AwsLambdaDeploy import AwsLambdaDeploy
from harc.system.HarcCliArguments import HarcCliArguments
import json

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
        project['repository'] = "https://'{0}':'{1}'@gitlab.et-scm.com/MDP/mdp-lambda.git"

        double = dict()
        double['dependencies'] = ['requests']
        la = dict()
        la['double.py'] = double

        lambdas = list()
        lambdas.append(la)

        register = dict()
        register['dependencies'] = ['requests']
        la = dict()
        la['register.py'] = register
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
        environment['aws_profile_name'] = 'default'
        environment['aws_bucket_name'] = 'elsevier-mdp-dev-source'
        environment['aws_region_name'] = 'eu-west-1'
        settings['dev'] = environment

        print(json.dumps(settings, indent=4, sort_keys=True))

        # Instantiate the parser
        parser = HarcCliArguments("harc = Hit And Release Code, probably python.")
        args = parser.parse_args(['aws:lambda:deploy', '-u', 'ripkej', '-p', 'Oxyma123'])

        plugin = AwsLambdaDeploy()
        plugin.execute(args, settings, properties)

        # the


if __name__ == '__main__':
    unittest.main()
