from harc.plugins.Plugin import Plugin
from harc.plugins.PluginException import PluginException
from harc.azure.AzContainerRegistry import AzContainerRegistry
from harc.system.Git import Git
from harc.system.System import System
from harc.system.Profile import Profile
from harc.system.Docker import Docker
from urllib.parse import urlparse, quote
from harc.shell.Key import Key
import uuid
import os


class AzContainerPush(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        self.set_command('az:container:push')

    def execute(self, arguments, settings, properties):

        # checkout the given version in a tmp_folder
        username = arguments.u
        password = arguments.p
        version = arguments.v
        environment = arguments.e
        resource_group = arguments.r

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
                    credentials = Profile.credentials(project['name'], properties)
                    if credentials:
                        username = credentials.get('username')
                        password = credentials.get('password')

                if not username:
                    raise PluginException("no username")

                if not password:
                    raise PluginException("no password")

                repository = url.scheme + "://'{0}':'{1}'@" + url.netloc + url.path
                repository = repository.format(quote(username), quote(password))

            # set identifier, reflecting the checkout folder to build this release.
            name = uuid.uuid4().hex

            # create an empty folder in tmp
            tmp_folder = System.recreate_tmp(name)

            # clone the repository to the tmp_folder
            result = Git.clone(repository, tmp_folder)
            print(result)

            # switch to given release, if present, otherwise the master is assumed
            # if not branch:
            #     branch = 'master'
            # result = Git.checkout_branch(branch, tmp_folder)
            # print("branch: " + str(result))

            if version:
                result = Git.checkout(version, tmp_folder)
                print(result)

            # retrieve the proxy settings of your system, and get it at https_proxy
            proxy = os.environ.get('https_proxy')
            proxy = Key.format('https_proxy', proxy)

            # build the docker image
            result = Docker.build(project['name'], tmp_folder, proxy)
            print(result)

            # retrieve
            registration = AzContainerRegistry.find_by_resource_group(resource_group=resource_group)

            if not registration:
                raise PluginException("registration not found")

            login_server = registration.get('loginServer')
            result = Docker.tag(project['name'], login_server, version)
            print(result)

            result = Docker.push(project['name'], login_server, version)
            print(result)

