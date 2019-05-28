from harc.plugins.Plugin import Plugin
from harc.plugins.PluginException import PluginException
from harc.system.Git import Git
from harc.system.System import System
from harc.system.Profile import Profile
from harc.system.Docker import Docker
from harc.plugins.UsernameOption import UsernameOption
from harc.plugins.PasswordOption import PasswordOption
from harc.plugins.EnvironmentOption import EnvironmentOption
from urllib.parse import urlparse, quote
from harc.shell.Key import Key
import uuid
import os
import click
import logging


class DockerBuild:

    @click.command()
    @click.option('-u', '--username', cls=UsernameOption, required=True)
    @click.option('-p', '--password', cls=PasswordOption, required=True)
    @click.option('-v', '--version', required=True, prompt='release version')
    @click.option('-e', '--environment', cls=EnvironmentOption, required=True)
    @click.pass_context
    def execute(ctx, username, password, version, environment):

        logger = logging.getLogger()
        logger.debug("username : {}, version: {}, environment : {}".format(username, version, environment))

        # retrieve the properties, set by the cli
        properties = ctx.obj

        project_name = properties['name']

        # parse the url, when the scheme is http or https a username, password combination is expected.
        url = urlparse(properties['repository'])
        repository = properties['repository']

        if url.scheme in ['http', 'https']:

            repository = url.scheme + "://'{0}':'{1}'@" + url.netloc + url.path
            repository = repository.format(quote(username), quote(password))

        # set identifier, reflecting the checkout folder to build this release.
        name = uuid.uuid4().hex

        # create an empty folder in tmp
        tmp_folder = System.recreate_tmp(name)

        # clone the repository to the tmp_folder
        print("Clone:")
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
        result = Docker.build(project_name, tmp_folder, version, proxy)
        print(result)
