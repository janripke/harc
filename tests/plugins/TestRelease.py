import uuid
import unittest
import os
from harc.plugins.GitRelease import GitRelease
from harc.system.HarcCliArguments import HarcCliArguments
from harc.system.Git import Git
from harc.system.System import System
from urlparse import urlparse
import urllib


class TestRelease(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ssh_release(self):
        properties = dict()
        properties['harc_dir'] = os.path.abspath('.')

        project = dict()
        project['name'] = 'mdp_lambda'
        project['technology'] = 'python'
        project['repository'] = 'ssh://git-codecommit.eu-west-1.amazonaws.com/v1/repos/mdp-lambda'

        projects = list()
        projects.append(project)

        settings = dict()
        settings['projects'] = projects

        # Instantiate the parser
        parser = HarcCliArguments("harc = Hit And Release Code, probably python.")
        args = parser.parse_args(None)

        plugin = GitRelease()
        plugin.execute(args, settings, properties)


if __name__ == '__main__':
    unittest.main()
