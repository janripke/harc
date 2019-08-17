import uuid
import os
import logging
from urllib.parse import urlparse, quote

import click

from harc.system.Git import Git
from harc.system.System import System
from harc.system.Docker import Docker
from harc.system.io.File import File
from harc.system.Requirements import Requirements
from harc.system.PropertyHelper import PropertyHelper

from harc.plugins.UsernameOption import UsernameOption
from harc.plugins.PasswordOption import PasswordOption
from harc.plugins.EnvironmentOption import EnvironmentOption

from harc.shell.Key import Key


class DockerBuild:
    @click.command()
    @click.option('-u', '--username', cls=UsernameOption, required=True)
    @click.option('-p', '--password', cls=PasswordOption, prompt=True, hide_input=True)
    @click.option('-v', '--version', required=False, prompt='release version')
    @click.option('-e', '--environment', cls=EnvironmentOption, required=True)
    @click.option('--checkout/--no-checkout')
    @click.pass_context
    def execute(ctx, username, password, version, environment, checkout):
        logger = logging.getLogger()
        logger.debug("username : {}, version: {}, environment : {}".format(username, version, environment))

        # retrieve the properties, set by the cli
        properties = ctx.obj

        project_name = properties['name']

        # parse the url, when the scheme is http or https a username, password combination is expected.
        url = urlparse(properties['repository'])
        repository = properties['repository']

        platform = PropertyHelper.find_platform(properties, environment, 'local')
        key_vault = PropertyHelper.find_key_vault(properties, environment)
        print("key_vault :", key_vault, type(key_vault))

        # Prepare repository checkout only if requested
        if checkout:
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
        else:
            tmp_folder = os.path.abspath('.')

        # Build a 'prepped' requirements file with injected user/pass tokens for http urls
        # Tokens will be taken from .git-credentials
        requirements = os.path.join(tmp_folder, 'requirements.txt')
        new_requirements = 'requirements_prepped.txt'
        logger.debug(requirements)
        if os.path.exists(requirements):
            credentials = Git.get_credentials()
            rf = File(requirements)
            rf_new = File(new_requirements)
            lines = rf.read_lines()
            lines = Requirements.tokenize(lines, credentials)
            rf_new.write_lines(lines)

        # retrieve the https proxy settings of your system
        proxy = os.environ.get('https_proxy')
        proxy = Key.format('https_proxy', proxy)

        # retrieve the proxy settings from your config.json in .harc
        if not proxy:
            proxy = properties.get('proxy')
            proxy = Key.format('https_proxy', proxy)

        # build the docker image
        result = Docker.build(
            project_name, tmp_folder, version, environment, platform, key_vault, proxy)

        if result:
            print("Build finished!")
        else:
            print("Build failed")
