from harc.plugins.Plugable import Plugable
from harc.plugins.PluginException import PluginException
from harc.system.Git import Git
from harc.system.System import System
from harc.system.PipUrl import PipUrl
from harc.system.io.Files import Files
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
        # todo: what bucket and subfolder are we going to use. I  will assume com-elsevier-mdp-deploy

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

            bucket_name = Settings.find_aws_bucket_name(settings, environment)
            print(bucket_name)

            profile_name = Settings.find_aws_profile_name(settings, environment)
            region_name = Settings.find_aws_region_name(settings, environment)

            # create the deploy bucket if not present.
            bucket = AwsBucket(profile_name, region_name)
            if not bucket.find(bucket_name):
                bucket.create(bucket_name)

            # archive the current emr deployment, if present.
            now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            response = bucket.list_objects(bucket_name, 'emr')
            files = response['files']
            for file in files:
                if not file['ContentType'] == 'application/x-directory':
                    path = file['Key']
                    dirname = os.path.dirname(path)
                    filename = os.path.basename(path)

                    # move the file to the archive location.
                    bucket.copy_object(bucket_name, path, bucket_name, os.path.join('archive', 'emr', now, path))
                    bucket.delete_object(bucket_name, path)

            # create the bootstrap.sh script.
            f = open(os.path.join(tmp_folder, 'bootstrap.sh'), 'wb')

            # find the bootstrap commands (dependencies) to included into bootstrap.sh
            bootstraps = Settings.list_bootstrap(settings, project_name)
            for bootstrap in bootstraps:

                # retrieve the bootstrap details
                module_name = bootstrap['name']
                module_version = bootstrap.get('version')
                module_repo = bootstrap.get('repository')

                statement = PipUrl.build(module_name, module_version, module_repo, username, password)
                statement = "pip install " + statement + '\n'
                f.write(statement.encode('utf-8'))

            # add the current project to bootstrap.sh
            statement = PipUrl.build(project_name, version, project['repository'], username, password)
            statement = "pip install " + statement + '\n'
            f.write(statement.encode('utf-8'))
            f.close()

            # upload the bootstrap file to aws
            bucket.upload(os.path.join(tmp_folder, 'bootstrap.sh'), bucket_name, 'emr/bootstrap/bootstrap.sh')

            steps = project['steps']
            for step in steps:

                excludes = ['__init__.py']
                files = Files.list(os.path.join(tmp_folder, project_name, step), excludes)
                for file in files:
                    path, filename = os.path.split(file)
                    bucket.upload(file, bucket_name, 'emr/steps/' + filename)



            # # find the files to deploy, they are expected in the module folder in the packages
            # # defined by find_lambdas.
            # find_lambdas = project['find_lambdas']
            # for find_lambda in find_lambdas:
            #
            #     excludes = ['__init__.py']
            #     files = Files.list(os.path.join(tmp_folder, project_name, find_lambda), excludes)
            #     for file in files:
            #         path, filename = os.path.split(file)
            #         basename, extension = os.path.splitext(filename)
            #
            #         build_name = uuid.uuid4().hex
            #         build_folder = System.create_tmp(build_name)
            #         print("building ", os.path.join(build_folder, basename + ".zip"))
            #
            #         # copy the project packages to the build folder.
            #         modules = Files.list(os.path.join(tmp_folder, project_name), find_lambdas)
            #         for module in modules:
            #             module_path, module_filename = os.path.split(module)
            #             module_path = module_path.replace(tmp_folder + os.sep, '')
            #
            #             # create the module folders in the build folder, if not present
            #             if not os.path.exists(os.path.join(build_folder, module_path)):
            #                 os.makedirs(os.path.join(build_folder, module_path))
            #
            #             # copy the module files to the module folders in the build folder.
            #             shutil.copy(module, os.path.join(build_folder, module_path, module_filename))
            #
            #         # copy the lambda module to build to the build folder.
            #         shutil.copyfile(file, os.path.join(build_folder, filename))
            #
            #         # find the dependencies of the module to build
            #         dependencies = Settings.list_dependencies(settings, project_name, filename)
            #         for dependency in dependencies:
            #
            #             # retrieve the dependency details
            #             module_name = dependency['name']
            #             module_version = dependency.get('version')
            #             module_repo = dependency.get('repository')
            #
            #             module = module_name
            #
            #             if module_version:
            #                 module = module_name + "==" + module_version
            #
            #             if module_repo:
            #                 module = module_repo
            #                 module_url = urlparse(module_repo)
            #
            #                 if module_url.scheme in ['http', 'https']:
            #                     if not username:
            #                         raise PluginException("no username")
            #
            #                     if not password:
            #                         raise PluginException("no password")
            #
            #                     module = "git+" + module_url.scheme + "://'{0}':'{1}'@" + module_url.netloc + module_url.path + " --upgrade --no-dependencies"
            #                     module = module.format(quote(username), quote(password))
            #
            #                     if module_version:
            #                         module = "git+" + module_url.scheme + "://'{0}':'{1}'@" + module_url.netloc + module_url.path + '@' + module_version + " --upgrade --no-dependencies"
            #                         module = module.format(quote(username), quote(password))
            #
            #             # install the configured module dependency into the build folder
            #             Pip.install(module, build_folder)
            #
            #         # set the filename and path of the zipped file to build
            #         zip_filename = basename + ".zip"
            #         zip_file = os.path.join(build_folder, zip_filename)
            #
            #         # add all the files in the temp folder to the zip file.
            #         # reflecting the module and its dependencies
            #         Zip.create(zip_file, build_folder)
            #
            #         # deploy the zipped file to aws
            #         # retrieve to aws profile_name to use, depending on the environment
            #         profile_name = Settings.find_aws_profile_name(settings, environment)
            #         region_name = Settings.find_aws_region_name(settings, environment)
            #         session = boto3.Session(profile_name=profile_name, region_name=region_name)
            #
            #         # upload the zipped file to the aws bucket.
            #         bucket_name = Settings.find_aws_bucket_name(settings, environment)
            #         print('deploying', os.path.join(build_folder, basename + ".zip"), "using profile", profile_name, "into bucket ",bucket_name)
            #         f = open(zip_file, "rb")
            #         aws_bucket = AwsBucket(session)
            #         aws_bucket.upload(f, bucket_name, zip_filename)
            #         f.close()
            #
            #         #
            #         code = dict()
            #         code['S3Bucket'] = bucket_name
            #         code['S3Key'] = zip_filename
            #
            #         aws_lambda = AwsLambda(session)
            #         lambda_function = aws_lambda.find_function(basename)
            #
            #         if lambda_function:
            #             aws_lambda.update_function_code(basename, code)
            #
