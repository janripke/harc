import unittest
import os
import harc
from harc.system.HarcCliArguments import HarcCliArguments
from harc.plugins.aws.generate.GeneratePlugin import Generate


class TestGenerate(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generate(self):
        properties = dict()
        properties['current.dir'] = os.path.abspath('.')
        properties['harc.dir'] = os.path.dirname(harc.__file__)
        properties['plugin.dir'] = os.path.join(properties.get('harc.dir'), 'plugins')

        # project name must reflect the project folder name in the git repo
        settings = {
            "project": {
                "name": "mdp_api",
                "technology": "python",
                "repository": "https://gitlab.et-scm.com/MDP/mdp-api.git",
                "dependencies": [
                    {
                        "name": "mdp_toolbox",
                        "technology": "python",
                        "repository": "https://gitlab.et-scm.com/MDP/mdp-toolbox.git",
                        "version": "1.0.8" #TODO: implement
                    }
                ]
            },
            "sandbox": {
                "aws_profile_name": "sandbox",
                "aws_region_name": "eu-west-1",
                "deploy_bucket_name": "elsevier-mdp-dev-deploy",
                "deploy_key_prefix": "eb/mdp_api/"
            },
            "build": {
                "aws_profile_name": "aws-bts-sandmnp",
                "aws_region_name": "eu-west-1",
                "deploy_bucket_name": "elsevier-mdp-dev-deploy",
                "deploy_key_prefix": "eb/mdp_api/"
            },
            "test": {
                "aws_profile_name": "elsevier-mdp-test",
                "aws_region_name": "eu-west-1",
                "deploy_bucket_name": "elsevier-mdp-dev-deploy",
                "deploy_key_prefix": "eb/mdp_api/"
            },
            "uat": {
                "aws_profile_name": "elsevier-mdp-uat",
                "aws_region_name": "eu-west-1",
                "deploy_bucket_name": "elsevier-mdp-dev-deploy",
                "deploy_key_prefix": "eb/mdp_api/"
            },
            "prod": {
                "aws_profile_name": "elsevier-mdp-prod",
                "aws_region_name": "eu-west-1",
                "deploy_bucket_name": "elsevier-mdp-dev-deploy",
                "deploy_key_prefix": "eb/mdp_api/"
            }
        }

        # Instantiate the parser
        parser = HarcCliArguments("harc = Hit And Release Code, probably python.")
        args = parser.parse_args(['aws:generate', '-t', 'lambda'])

        plugin = Generate()
        print(args)
        print(settings)
        print(properties)
        plugin.execute(args, settings, properties)