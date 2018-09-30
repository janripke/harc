from harc.plugins.Plugable import Plugable
from harc.plugins.PluginException import PluginException
from harc.system.Git import Git
from harc.system.System import System
from harc.system.PipUrl import PipUrl
from harc.system.io.Files import Files
from harc.system.Toolbox import Toolbox
from harc.system.Package import Package
from harc.system.logger.Logger import Logger
from harc.system.Traceback import Traceback
from harc.system.Settings import Settings
from harc.system.Pip import Pip
from harc.system.Zip import Zip
from harc.amazon.AwsBucket import AwsBucket
from harc.amazon.AwsLambda import AwsLambda
from urllib.parse import urlparse, quote
from datetime import datetime
import urllib
import uuid
import os
import shutil
import boto3


class AwsEmrDeploy(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def execute(arguments, settings, properties):

        # checkout the given version in a tmp_folder
        # create the bootstrap script containing the python dependencies.
        # remove all the files in the emr s3 deployment folder (steps) by archiving them.
        # upload the bootstrap script to the desired bucket (bucket.deploy/emr)
        # upload all the steps to bucket.deploy/emr/steps

        #
        # when emr starts, the steps folder is scanned, all the files will be part of the execution.

        username = arguments.u
        password = arguments.p
        version = arguments.v
        environment = arguments.e

        # if no environment is given dev is assumed.
        if not environment:
            environment = 'dev'

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
            if version:
                result = Git.checkout_tag(tmp_folder, version)
                print("tag: " + str(result))

            bucket_name = Settings.find_deploy_bucket_name(settings, environment)
            print(bucket_name)

            profile_name = Settings.find_aws_profile_name(settings, environment)
            region_name = Settings.find_aws_region_name(settings, environment)

            Toolbox.archive(profile_name, region_name, bucket_name, 'emr')

            # create the bootstrap.sh script.
            f = open(os.path.join(tmp_folder, 'bootstrap.sh'), 'wb')

            # retrieve the credentials method
            git_username = None
            git_password = None
            credentials_method = project['credentials']
            if credentials_method == 'ldap':
                # use parameters add bootstrap, to avoid they are part of the release.
                git_username = '$1'
                git_password = '$2'

            # find the bootstrap commands (dependencies) to included into bootstrap.sh
            bootstraps = Settings.list_bootstrap(settings, project_name)
            for bootstrap in bootstraps:

                # retrieve the bootstrap details
                module_name = bootstrap['name']
                module_version = bootstrap.get('version')
                module_repo = bootstrap.get('repository')
                module_type = bootstrap.get('type')

                if module_type == 'pip':
                    statement = PipUrl.build(module_name, module_version, module_repo, git_username, git_password, False, True)
                    statement = "sudo python3.4 -m pip install " + statement + '\n'
                if module_type == 'yum':
                    statement = "which git || sudo yum install " + module_name + ' -y' + '\n'
                f.write(statement.encode('utf-8'))

            # add the current project to bootstrap.sh
            statement = PipUrl.build(project_name, version, project['repository'], git_username, git_password, False, True)
            statement = "sudo python3.4 -m pip install " + statement + '\n'
            f.write(statement.encode('utf-8'))
            f.close()

            # raise exception if the deploy bucket is not present.
            bucket = AwsBucket(profile_name, region_name)
            if not bucket.find(bucket_name):
                raise PluginException("deployment bucket {} not found".format(bucket_name))

            # upload the bootstrap file to aws
            bucket.upload(os.path.join(tmp_folder, 'bootstrap.sh'), bucket_name, 'emr/bootstrap/bootstrap.sh')

            steps = project['steps']
            for step in steps:

                excludes = ['__init__.py']
                files = Files.list(os.path.join(tmp_folder, project_name, step), excludes)
                for file in files:
                    path, filename = os.path.split(file)
                    bucket.upload(file, bucket_name, 'emr/steps/' + filename)
