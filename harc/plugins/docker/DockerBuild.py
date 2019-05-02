from harc.plugins.Plugable import Plugable
from harc.plugins.PluginException import PluginException
from harc.system.Git import Git
from harc.system.System import System
from urllib.parse import urlparse, quote
import uuid


class DockerBuild(Plugable):
    def __init__(self):
        Plugable.__init__(self)

    @staticmethod
    def execute(arguments, settings, properties):
        pass

        # checkout the given version in a tmp_folder
        username = arguments.u
        password = arguments.p
        version = arguments.v
        environment = arguments.e

        # if no environment is given local is assumed.
        if not environment:
            environment = 'local'

        projects = settings['projects']
        for project in projects:

            project_name = project['name']

            # parse the url, when the scheme is http or https a username, password combination is expected.
            url = urlparse(project['repository'])
            repository = project['repository']

            if url.scheme in ['http', 'https']:
                if not username:
                    raise PluginException("no username")

                if not password:
                    raise PluginException("no password")

                repository = url.scheme + "://'{0}':'{1}'@" + url.netloc + url.path
                repository = repository.format(quote(username), quote(password))

            # set identifier, reflecting the checkout folder to build this release.
            name = uuid.uuid4().hex

            # create an empty folder in tmp
            tmp_folder = System.create_tmp(name)

            # clone the repository to the tmp_folder
            result = Git.clone(repository, tmp_folder)
            print("clone: " + str(result))

            # switch to given release, if present, otherwise the master is assumed
            # if not branch:
            #     branch = 'master'
            # result = Git.checkout_branch(branch, tmp_folder)
            # print("branch: " + str(result))

            if version:
                result = Git.checkout(version, tmp_folder)
                print("version: " + str(result))

