import unittest
from harc.amazon.AwsIam import AwsIam
from harc.system.Settings import Settings
import boto3


class TestAwsIam(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_deploy(self):
        settings = dict()

        env = dict()
        env['aws_profile_name'] = 'elsevier-mdp-dev'
        env['aws_bucket_name'] = 'elsevier-mdp-dev-source'
        env['aws_region_name'] = 'eu-west-1'
        settings['dev'] = env

        environment = 'dev'
        profile_name = Settings.find_aws_profile_name(settings, environment)
        region_name = Settings.find_aws_region_name(settings, environment)
        print 'using profile :', profile_name
        print 'using region :', region_name
        session = boto3.Session(profile_name=profile_name, region_name=region_name)

        aws_iam = AwsIam(session)
        role = aws_iam.find_role('LambdaExecution')
        print role


if __name__ == '__main__':
    unittest.main()
