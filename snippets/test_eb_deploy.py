from harc.amazon.AwsBucket import AwsBucket
from harc.system.System import System
from harc.system.Pip import Pip
from harc.system.Zip import Zip

import boto3
import os
import uuid
from datetime import datetime


profile_name = 'sandbox'
region_name = 'eu-west-1'

bucket_name = 'elsevier-mdp-dev-deploy'
key_prefix = 'eb/mdp_api/'

#target_files
source_paths = ["/home/user/workspace/mdp-api/mdp_api",
                "/home/user/workspace/mdp-toolbox/mdp_toolbox",
                "/home/user/workspace/mdp-api/requirements.txt"]

# create the deploy bucket if not present.
bucket = AwsBucket(profile_name, region_name)
if not bucket.find(bucket_name):
    bucket.create(bucket_name)

now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

# archive the current emr deployment, if present.
response = bucket.list_objects(bucket_name, key_prefix)
files = response['files']
for fle in files:
    if not fle['ContentType'] == 'application/x-directory':
        path = fle['Key']
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)

        # move the file to the archive location.
        bucket.copy_object(bucket_name, path, bucket_name, os.path.join('archive', 'eb', now, filename))
        bucket.delete_object(bucket_name, path)

# set identifier, reflecting the checkout folder to build this release.
name = uuid.uuid4().hex

# create an empty folder in tmp
tmp_folder = System.recreate_tmp(name)

# Copy the required projects into the temporary folder
for path in source_paths:
    System.copy(path, os.path.join(tmp_folder, path.split("/")[-1]))

# set the filename and path of the zipped file to build
basename = "mdp_api_source_bundle_" + now.strip()
print(basename)
zip_filename = basename + ".zip"
zip_file = os.path.join(tmp_folder, zip_filename)
key = key_prefix + zip_filename


# add all the files in the temp folder to the zip file.
# reflecting the module and its dependencies
Zip.create(zip_file, tmp_folder)

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


