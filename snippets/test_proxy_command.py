import unittest
from harc.shell.parameter import Parameter
from harc.shell.command import Command


class TestCommand(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_command(self):

        resource_group = "sandbox-nl02329-001-rg"
        subscription = 'AABNL AZ Lab'

        statement = "az keyvault list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))

        env_vars = dict(https_proxy='nl-userproxy-access.net.abnamro.com:8080')
        output = Command.execute(statement, env=env_vars)

        keyvaults = Command.jsonify(output)
        keyvault = keyvaults[0]
        keyvault_name = keyvault.get('name')

        expected = 'cbca-s-kv'
        self.assertEqual(expected, keyvault_name, 'invalid keyvault name')