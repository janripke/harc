from harc.harc_cli import main
import unittest


class TestDockerBuild(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_buid(self):
        main(['docker:build', '-u', '****', '-p', '****', '-e', 'dev', '-v', '1.0.0'])


if __name__ == '__main__':
    unittest.main()
