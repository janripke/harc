import unittest
import os
from harc.plugins.pypi.PyPiDeploy import PyPiDeploy
from harc.system.HarcCliArguments import HarcCliArguments


class TestRelease(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pypi_deploy(self):
        properties = dict()
        properties['harc_dir'] = os.path.abspath('.')

        project = dict()
        project['name'] = 'harc'
        project['technology'] = 'python'
        project['repository'] = "https://github.com/janripke/harc.git"

        projects = list()
        projects.append(project)

        settings = dict()
        settings['projects'] = projects

        # Instantiate the parser
        parser = HarcCliArguments("harc = Hit And Release Code, probably python.")
        args = parser.parse_args(['pypi:deploy', '-u', 'janripke', '-p', '*****', '-v', '1.0.15'])

        plugin = PyPiDeploy()
        plugin.execute(args, settings, properties)


if __name__ == '__main__':
    unittest.main()
