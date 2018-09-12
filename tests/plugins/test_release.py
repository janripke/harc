import unittest
import os
from harc.plugins.git.GitRelease import GitRelease
from harc.system.HarcCliArguments import HarcCliArguments



class TestRelease(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_https_release(self):
        properties = dict()
        properties['harc_dir'] = os.path.abspath('.')

        project = dict()
        project['name'] = 'mdp_lambda'
        project['technology'] = 'python'
        project['repository'] = "https://gitlab.et-scm.com/MDP/mdp-lambda.git"

        projects = list()
        projects.append(project)

        settings = dict()
        settings['projects'] = projects

        # Instantiate the parser
        parser = HarcCliArguments("harc = Hit And Release Code, probably python.")
        args = parser.parse_args(['git:release', '-u', 'ripkej', '-p', '*******'])

        plugin = GitRelease()
        plugin.execute(args, settings, properties)


if __name__ == '__main__':
    unittest.main()
