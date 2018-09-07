from harc.plugins.Plugable import Plugable
from harc.plugins.PluginException import PluginException
from harc.plugins.RequirementsException import RequirementsException
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

        # if no environment is given sandbox is assumed.
        if not environment:
            environment = 'sandbox'

        project = settings['project']
        project_name = project['name']

        # retrieve aws profile_name to use, depending on the environment
        profile_name = Settings.find_aws_profile_name(settings, environment)
        region_name = Settings.find_aws_region_name(settings, environment)

        # retrieve upload bucket name and key prefix.
        bucket_name = Settings.find_deploy_bucket_name(settings, environment)
        key_prefix = Settings.find_deploy_key_prefix(settings, environment)

        # set identifier, reflecting the checkout folder to build this release.
        name = uuid.uuid4().hex
        tmp_folder = System.create_tmp(name)
        # required files are copied into build_folder that is zipped and uploaded to s3
        build_folder = System.create_tmp(name, "build_folder")

        #Clone the repo into the temp folder
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

        Git.clone(repository, os.path.join(tmp_folder, project_name))
        System.copy(os.path.join(os.path.join(tmp_folder, project_name), project_name), os.path.join(build_folder, project_name))

        try: #TODO: Test??
            System.copy(os.path.join(os.path.join(tmp_folder, project_name), "requirements.txt"), build_folder)
        except RequirementsException:
            RequirementsException("no requirements.txt. Run 'pip freeze >requirements.txt' in the project folder and "
                                  "push the generated requirements.txt file into the git repo.")

        if project['dependencies']:
            for dependency in project['dependencies']:
                # parse the url, when the scheme is http or https a username, password combination is expected.
                url = urlparse(dependency['repository'])
                repository = dependency['repository']
                dependency_name = dependency['name']

                if url.scheme in ['http', 'https']:
                    if not username:
                        raise PluginException("no username")

                    if not password:
                        raise PluginException("no password")

                    repository = url.scheme + "://'{0}':'{1}'@" + url.netloc + url.path
                    repository = repository.format(quote(username), quote(password))

                Git.clone(repository, os.path.join(tmp_folder, dependency_name))
                System.copy(os.path.join(tmp_folder, dependency_name, dependency_name), os.path.join(build_folder, dependency_name))

        # set the filename and path of the zipped file to build
        now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        basename = project_name + "_source_bundle_" + now.strip()
        zip_filename = basename + ".zip"
        zip_file = os.path.join(build_folder, zip_filename)
        key = key_prefix + zip_filename

        print('Creating {} under {} folder'.format(zip_filename, build_folder))
        # add all the files in the temp folder to the zip file.
        # reflecting the module and its dependencies
        Zip.create(zip_file, build_folder)


        # upload the zipped file to aws
        print('uploading the zip file using profile', profile_name, "into bucket ", bucket_name, "and key", key)
        aws_bucket = AwsBucket(profile_name, region_name)
        aws_bucket.upload(zip_file, bucket_name, key)

        # create new application version on eb with the uploaded source bundle
        client = boto3.client('elasticbeanstalk')

        eb_application_name = project_name + '-' + environment
        eb_environment_name = eb_application_name + '-env'
        application_update_ts = now
        if version:
            version_label = version
        else:
            version_label = 'harc_deployment_{}'.format(application_update_ts)

        response = client.create_application_version(
            ApplicationName=eb_application_name,
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
                ApplicationName=eb_application_name,
                VersionLabels=[version_label],
            )
            response = response.get('ApplicationVersions')[0]
            print(response)

        response = client.update_environment(
            ApplicationName=response.get('ApplicationName'),
            VersionLabel=response.get('VersionLabel'),
            EnvironmentName=eb_environment_name
        )
        print(response)



