import unittest
import os
from harc.plugins.aws.AwsLambdaDeploy import AwsLambdaDeploy
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

        # create the project main part
        project = dict()
        project['name'] = 'mdp_lambda'
        project['technology'] = 'python'
        project['repository'] = "https://gitlab.et-scm.com/MDP/mdp-lambda.git"

        # create lambdas part
        find_lambdas = list()
        find_lambdas.append("lambdas")
        project['find_lambdas'] = find_lambdas

        # create dependency part
        module_list = list()

        module = dict()
        module['name'] = "requests"
        module_list.append(module)

        module = dict()
        module['name'] = "mdp_toolbox"
        # module['version'] = "1.0.1"
        module['repository'] = "https://gitlab.et-scm.com/MDP/mdp-toolbox.git"
        module_list.append(module)

        dependencies = dict()
        dependencies['double.py'] = module_list
        dependencies['register.py'] = module_list

        project['dependencies'] = dependencies

        projects = list()
        projects.append(project)

        # create the environment part
        settings = dict()
        settings['projects'] = projects

        environment = dict()
        environment['name_pattern'] = '{{basename}}-{{environment}}'
        environment['aws_profile_name'] = 'default'
        environment['deploy_bucket_name'] = 'elsevier-mdp-dev-deploy'
        environment['aws_region_name'] = 'eu-west-1'
        settings['sandbox'] = environment

        print(json.dumps(settings, indent=4, sort_keys=True))

        # Instantiate the parser
        parser = HarcCliArguments("harc = Hit And Release Code, probably python.")
        args = parser.parse_args(['aws:lambda:deploy', '-u', 'ripkej', '-p', '*'])

        plugin = AwsLambdaDeploy()
        plugin.execute(args, settings, properties)


if __name__ == '__main__':
    unittest.main()
