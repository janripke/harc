from harc.plugins.Plugable import Plugable
from harc.plugins.PluginException import PluginException
from harc.plugins.RequirementsException import RequirementsException
from harc.system.Git import Git
from harc.system.System import System
from harc.system.Settings import Settings
from harc.system.Zip import Zip
from harc.amazon.AwsBucket import AwsBucket
from urllib.parse import urlparse, quote
from datetime import datetime
import uuid
import os
import boto3


class AwsEc2Deploy(Plugable):
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
            environment = 'build'

        project = settings['project']
        project_name = project['name']

        # retrieve aws profile_name to use, depending on the environment
        profile_name = Settings.find_aws_profile_name(settings, environment)
        region_name = Settings.find_aws_region_name(settings, environment)

        # retrieve upload bucket name and key prefix.
        bucket_name = Settings.find_deploy_bucket_name(settings, environment)
        key_prefix_live = Settings.find_deploy_key_prefix_live(settings, environment)
        key_prefix_archive = Settings.find_deploy_key_prefix_archive(settings, environment)

        # set identifier, reflecting the checkout folder to build this release.
        name = uuid.uuid4().hex
        tmp_folder = System.create_tmp(name)
        # required files are copied into build_folder that is zipped and uploaded to s3
        build_folder = System.create_tmp(name, "build_folder")

        # Clone the repo into the temp folder
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

        print('Cloning {} from the git repo...'.format(project_name))
        Git.clone(repository, os.path.join(tmp_folder, project_name))

        # switch to given release, if present, otherwise the master is assumed
        # if not branch:
        #     branch = 'master'
        # result = Git.checkout_branch(branch, os.path.join(tmp_folder, project_name))
        # print("branch: " + str(result))

        if version:
            result = Git.checkout(version, os.path.join(tmp_folder, project_name))
            print('Git tag "{}" is used for version {}...'.format(result, version))

        # Copy the
        System.copy(os.path.join(tmp_folder, project_name, project_name), os.path.join(build_folder, project_name))

        try:
            System.copy(os.path.join(os.path.join(tmp_folder, project_name), "requirements.txt"), build_folder)
        except RequirementsException:
            RequirementsException("No requirements.txt is found. Run 'pip freeze >requirements.txt' in the project folder and "
                                  "push the generated requirements.txt file into the git repo.")

        if project['dependencies']:
            for dependency in project['dependencies']:
                # parse the url, when the scheme is http or https a username, password combination is expected.
                url = urlparse(dependency['repository'])
                repository = dependency['repository']
                dependency_name = dependency['name']
                dependency_version = dependency['version']

                if url.scheme in ['http', 'https']:
                    if not username:
                        raise PluginException("no username")

                    if not password:
                        raise PluginException("no password")

                    repository = url.scheme + "://'{0}':'{1}'@" + url.netloc + " -b '{2}' " + url.path
                    repository = repository.format(quote(username), quote(password), quote(dependency_version))

                print('WARNING: HARC expects requirements.txt in your repo. Use "pip freeze >requirements.txt" command '
                      'to create it in a virtual environment that can run the project')
                print('Cloning {} from the git repo...'.format(dependency_name))
                Git.clone(repository, os.path.join(tmp_folder, dependency_name))

                # # switch to given release, if present, otherwise the master is assumed
                # if not branch:
                #     branch = 'master'
                # result = Git.checkout_branch(branch, os.path.join(tmp_folder, project_name))
                # print("branch: " + str(result))
                #
                # if version:
                #     result = Git.checkout(version, os.path.join(tmp_folder, project_name))
                #     print('Git tag/branch "{}" is used for version {}...'.format(result, version))

                System.copy(os.path.join(tmp_folder, dependency_name, dependency_name), os.path.join(build_folder, dependency_name))

        # set the filename and path of the zipped file to build for archive
        now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        basename = project_name + "_source_bundle"
        basename_ts = basename + "_" + now.strip()

        zip_filename_archive = basename_ts + ".zip"
        zip_file_archive = os.path.join(build_folder, zip_filename_archive)

        # set the filename and path of the zipped file to build for live
        zip_filename_live = basename + ".zip"
        zip_file_live = os.path.join(build_folder, zip_filename_live)

        # set key names for archive and live
        key_live = key_prefix_live + zip_filename_live
        key_archive = key_prefix_archive + zip_filename_archive


        print('Creating {} under {} folder'.format(zip_filename_archive, build_folder))
        # add all the files in the temp folder to the zip file.
        # reflecting the module and its dependencies
        Zip.create(zip_file_archive, build_folder)

        # upload the zipped file to aws
        print('Uploading the zip file using profile "{}" into bucket "{}" and key "{}"'.format(profile_name, bucket_name, key_archive))
        bucket = AwsBucket(profile_name, region_name)
        bucket.upload(zip_file_archive, bucket_name, key_archive)

        os.rename(zip_file_archive, zip_file_live)
        bucket.upload(zip_file_live, bucket_name, key_live)




