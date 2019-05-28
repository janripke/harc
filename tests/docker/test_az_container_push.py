from harc.harc_cli import main
import unittest


class TestDockerBuild(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_buid(self):
        main(['az:container:push', '-v', '1.0.1'])


if __name__ == '__main__':
    unittest.main()
