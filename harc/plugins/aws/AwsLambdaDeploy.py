from harc.plugins.Plugable import Plugable
from harc.plugins.PluginException import PluginException
from harc.system.Git import Git
from harc.system.System import System
from harc.system.io.Files import Files
from harc.system.Toolbox import Toolbox
from harc.system.VariableFilter import VariableFilter
from harc.system.ExpressionParser import ExpressionParser
from harc.system.Package import Package
from harc.system.logger.Logger import Logger
from harc.system.Traceback import Traceback
from harc.system.Settings import Settings
from harc.system.Pip import Pip
from harc.system.Zip import Zip
from harc.amazon.AwsBucket import AwsBucket
from harc.amazon.AwsLambda import AwsLambda
from urllib.parse import urlparse, quote
from harc.system.PipUrl import PipUrl
import urllib
import uuid
import os
import shutil
import boto3


class AwsLambdaDeploy(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def execute(arguments, settings, properties):

        username = arguments.u
        password = arguments.p
        version = arguments.v
        environment = arguments.e

        # if no environment is given build is assumed.
        if not environment:
            environment = 'build'

        projects = settings['projects']
        print(projects)
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

            # retrieve aws profile_name to use, depending on the environment
            profile_name = Settings.find_aws_profile_name(settings, environment)
            region_name = Settings.find_aws_region_name(settings, environment)

            # retrieve upload bucket name.
            bucket_name = Settings.find_deploy_bucket_name(settings, environment)

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

            Toolbox.archive(profile_name, region_name, bucket_name, 'lambda')

            # find the files to deploy, they are expected in the module folder in the packages
            # defined by find_lambdas.
            find_lambdas = project['find_lambdas']
            for find_lambda in find_lambdas:

                excludes = ['__init__.py']
                files = Files.list(os.path.join(tmp_folder, project_name, find_lambda), excludes)
                for file in files:
                    path, filename = os.path.split(file)
                    basename, extension = os.path.splitext(filename)

                    build_name = uuid.uuid4().hex
                    build_folder = System.create_tmp(build_name)
                    print("building ", os.path.join(build_folder, basename + ".zip"))

                    # copy the project packages to the build folder.
                    modules = Files.list(os.path.join(tmp_folder, project_name), find_lambdas)
                    for module in modules:
                        module_path, module_filename = os.path.split(module)
                        module_path = module_path.replace(tmp_folder + os.sep, '')

                        # create the module folders in the build folder, if not present
                        if not os.path.exists(os.path.join(build_folder, module_path)):
                            os.makedirs(os.path.join(build_folder, module_path))

                        # copy the module files to the module folders in the build folder.
                        shutil.copy(module, os.path.join(build_folder, module_path, module_filename))

                    # copy the lambda module to build to the build folder.
                    shutil.copyfile(file, os.path.join(build_folder, filename))

                    # find the dependencies of the module to build
                    dependencies = Settings.list_dependencies(settings, project_name, filename)
                    for dependency in dependencies:

                        # retrieve the dependency details
                        module_name = dependency['name']
                        module_version = dependency.get('version')
                        module_repo = dependency.get('repository')

                        # build the pip url
                        module = PipUrl.build(module_name, module_version, module_repo, username, password)

                        # install the configured module dependency into the build folder
                        Pip.install(module, build_folder)

                    # set the filename and path of the zipped file to build
                    zip_filename = basename + ".zip"
                    zip_file = os.path.join(build_folder, zip_filename)

                    # add all the files in the temp folder to the zip file.
                    # reflecting the module and its dependencies
                    Zip.create(zip_file, build_folder)

                    # deploy the zipped file to aws
                    print('deploying', os.path.join(build_folder, basename + ".zip"), "using profile", profile_name, "into bucket ",bucket_name)
                    aws_bucket = AwsBucket(profile_name, region_name)
                    aws_bucket.upload(zip_file, bucket_name, 'lambda/' + zip_filename)

                    #
                    code = dict()
                    code['S3Bucket'] = bucket_name
                    code['S3Key'] = 'lambda/' + zip_filename

                    # retrieve name_pattern to use, depending on the environment
                    # the name_pattern can be empty, indicating that it is not used.
                    name_pattern = Settings.find_name_pattern(settings, environment)

                    print("name_pattern:", name_pattern)

                    if name_pattern:
                        # retrieve a map containing the values of the given variables
                        maps = VariableFilter.filter(locals(), ['basename', 'environment'])

                        # retrieve the basename, based on the given name_pattern
                        basename = ExpressionParser.parse(name_pattern, maps)
                        print("basename:", basename)

                    aws_lambda = AwsLambda(profile_name, region_name)
                    lambda_function = aws_lambda.find_function(basename)
                    print("lambda_function:", lambda_function)

                    if lambda_function:
                        print('updating lambda function ' + basename)
                        aws_lambda.update_function_code(basename, code)

