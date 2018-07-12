from harc.plugins.Plugable import Plugable
from harc.system.System import System
from harc.system.Git import Git
from harc.plugins.PluginException import PluginException
import urllib


class GitBranches(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def execute(arguments, settings, properties):
        projects = settings['projects']
        username = arguments.u
        password = arguments.p

        if not username:
            raise PluginException("no username")

        if not password:
            raise PluginException("no password")

        project = projects[0]
        repository = project['repository'].format(urllib.quote(username), urllib.quote(password))

        # create an empty folder in tmp
        tmp_folder = System.create_tmp(project['name'])

        # clone the repository to the tmp_folder
        result = Git.clone(repository, tmp_folder)
        print "clone: " + str(result)

        # retieve the branches
        branches = Git.branches(tmp_folder)
        for branch in branches:
            print 'branch: ' + branch


