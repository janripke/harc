from harc.plugins.Plugable import Plugable
from harc.plugins.PluginException import PluginException
from harc.system.Git import Git
from harc.system.System import System
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
from harc.system.PipUrl import PipUrl
from datetime import datetime
import urllib
import uuid
import os
import shutil
import boto3


class AwsEbDeploy(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def execute(arguments, settings, properties):
        username = arguments.u
        password = arguments.p
        version = arguments.v
        environment = arguments.e

        profile_name = 'sandbox'
        region_name = 'eu-west-1'

        bucket_name = 'elsevier-mdp-dev-deploy'
        key_prefix = 'eb/mdp_api/'

        now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

        # if no environment is given sandbox is assumed.
        if not environment:
            environment = 'sandbox'

        project = settings['project']
        project_name = project['name']

        # parse the url, when the scheme is http or https a username, password combination is expected.
        url = urlparse(project['repository'])
        repository = project['repository']

        if url.scheme in ['http', 'https']:
            if not username:
                raise PluginException("no username")

            if not password:
                raise PluginException("no password")

            # repository = url.scheme + "://'{0}':'{1}'@" + url.netloc + url.path
            # repository = repository.format(quote(username), quote(password))

        # retrieve aws profile_name to use, depending on the environment
        profile_name = Settings.find_aws_profile_name(settings, environment)
        region_name = Settings.find_aws_region_name(settings, environment)

        # retrieve upload bucket name.
        bucket_name = Settings.find_aws_bucket_name(settings, environment)

        # set identifier, reflecting the checkout folder to build this release.
        name = uuid.uuid4().hex

        # create an empty folder in tmp
        build_folder = System.create_tmp(name)







        module_name = project_name
        module_version = None
        module_repo = repository
        module_type = 'pip'

        module = PipUrl.build(module_name, module_version, module_repo, username, password, no_dependencies=False)

        print(build_folder)
        if module_type == 'pip':
            result = Pip.install(module, build_folder)
            print(result)
        # if module_type == 'yum':
        #     result = "which git || sudo yum install " + module_name + ' -y' + '\n'



        # check for explicit dependencies that needs to be installed

        if project['dependencies']:
            for dependency in project['dependencies']:
                module_name = dependency['name']
                module_version = dependency.get('version')
                module_repo = dependency.get('repository')
                module_type = dependency.get('type')
                module = PipUrl.build(module_name, module_version, module_repo, username, password,
                                      no_dependencies=False)

                if module_type == 'pip':
                    result = Pip.install(module, build_folder)
                    print(result)

        # set the filename and path of the zipped file to build
        basename = "mdp_api_source_bundle_" + now.strip()
        print(basename)
        zip_filename = basename + ".zip"
        zip_file = os.path.join(build_folder, zip_filename)
        key = key_prefix + zip_filename

        # add all the files in the temp folder to the zip file.
        # reflecting the module and its dependencies
        Zip.create(zip_file, build_folder)

        # upload the zipped file to aws
        print('uploading', zip_file, "using profile", profile_name, "into bucket ", bucket_name)
        aws_bucket = AwsBucket(profile_name, region_name)
        aws_bucket.upload(zip_file, bucket_name, key)

        # create new application version on eb with the uploaded source bundle
        client = boto3.client('elasticbeanstalk')

        application_name = 'mdp-api-sandbox'
        environment_name = application_name + '-env'
        application_update_ts = now
        version_label = 'harc_deployment_{}'.format(application_update_ts)

        response = client.create_application_version(
            ApplicationName=application_name,
            VersionLabel=version_label,
            Description='{} deployed on {}'.format(basename, application_update_ts),
            SourceBundle={
                'S3Bucket': 'elsevier-mdp-dev-deploy',
                'S3Key': key_prefix + zip_filename
            },
            AutoCreateApplication=False,
            Process=True
        )
        response = response.get('ApplicationVersion')
        print(response)
        while response.get('Status') == 'PROCESSING':
            response = client.describe_application_versions(
                ApplicationName=application_name,
                VersionLabels=[version_label],
            )
            response = response.get('ApplicationVersions')[0]
            print(response)

        response = client.update_environment(
            ApplicationName=response.get('ApplicationName'),
            VersionLabel=response.get('VersionLabel'),
            EnvironmentName=environment_name
        )



