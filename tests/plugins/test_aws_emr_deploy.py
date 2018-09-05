import unittest
import os
from harc.plugins.AwsEmrDeploy import AwsEmrDeploy
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
        project['name'] = "mdp_emr"
        project['technology'] = "python"
        project['repository'] = "https://gitlab.et-scm.com/MDP/mdp-emr.git"

        # create bootstrap part
        bootstraps = list()

        # add bootstrap item git
        bootstrap = dict()
        bootstrap['name'] = "git"
        bootstrap['type'] = "yum"
        bootstraps.append(bootstrap)

        # add bootstrap item awscli
        bootstrap = dict()
        bootstrap['name'] = "awscli"
        bootstrap['type'] = "pip"
        bootstraps.append(bootstrap)

        # add bootstrap item mdp_toolbox
        bootstrap = dict()
        bootstrap['name'] = "mdp_toolbox"
        bootstrap['type'] = "pip"
        bootstrap['version'] = "1.0.8"
        bootstrap['repository'] = "https://gitlab.et-scm.com/MDP/mdp-toolbox.git"
        bootstraps.append(bootstrap)

        project['bootstrap'] = bootstraps

        # create steps part
        steps = list()
        steps.append("steps")
        project['steps'] = steps

        projects = list()
        projects.append(project)

        # create the environment part
        settings = dict()
        settings['projects'] = projects

        environment = dict()
        environment['aws_profile_name'] = 'default'
        environment['aws_bucket_name'] = 'elsevier-mdp-dev-deploy'
        environment['aws_region_name'] = 'eu-west-1'
        settings['dev'] = environment

        print(json.dumps(settings, indent=4, sort_keys=True))

        # Instantiate the parser
        parser = HarcCliArguments("harc = Hit And Release Code, probably python.")
        args = parser.parse_args(['aws:emr:deploy', '-u', 'ripkej', '-p', 'Oxyma123'])

        plugin = AwsEmrDeploy()
        plugin.execute(args, settings, properties)


if __name__ == '__main__':
    unittest.main()
