import unittest
import os
from harc.plugins.AwsEbDeploy import AwsEbDeploy
from harc.system.HarcCliArguments import HarcCliArguments
import json


class TestEbDeploy(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_deploy(self):
        properties = dict()
        properties['harc_dir'] = os.path.abspath('.')

        settings = {
          "project": {
            "name": "mdp_api",
            "technology": "python",
            "repository": "https://gitlab.et-scm.com/MDP/mdp-api.git",
            "dependencies": [
              {
                "name": "mdp_toolbox",
                "technology": "python",
                "type": "pip",
                "repository": "https://gitlab.et-scm.com/MDP/mdp-toolbox.git"
              }
            ]
          },
          "sandbox": {
            "aws_profile_name": "sandbox",
            "aws_bucket_name": "elsevier-mdp-dev-deploy",
            "aws_region_name": "eu-west-1"
          },
          "build": {
            "aws_profile_name": "aws-bts-sandmnp",
            "aws_bucket_name": "elsevier-mdp-dev-deploy",
            "aws_region_name": "eu-west-1"
          },
          "test": {
            "aws_profile_name": "elsevier-mdp-test",
            "aws_bucket_name": "elsevier-mdp-test-deploy",
            "aws_region_name": "eu-west-1"
          },
          "uat": {
            "aws_profile_name": "elsevier-mdp-uat",
            "aws_bucket_name": "elsevier-mdp-uat-deploy",
            "aws_region_name": "eu-west-1"
          },
          "prod": {
            "aws_profile_name": "elsevier-mdp-prod",
            "aws_bucket_name": "elsevier-mdp-deploy",
            "aws_region_name": "eu-west-1"
          }
        }

        # Instantiate the parser
        parser = HarcCliArguments("harc = Hit And Release Code, probably python.")
        args = parser.parse_args(['aws:eb:deploy', '-u', 'ripkej', '-p', 'Oxyma123'])

        plugin = AwsEbDeploy()
        print(args)
        print(settings)
        print(properties)
        plugin.execute(args, settings, properties)

