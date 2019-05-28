from harc.amazon.AwsBucket import AwsBucket
from harc.system.System import System
from harc.system.Settings import Settings
from os.path import basename
import os
import uuid
from datetime import datetime

profile_name = 'default'
region_name = 'eu-west-1'

bucket_name = 'elsevier-mdp-dev-deploy'

# create the deploy bucket if not present.
bucket = AwsBucket(profile_name, region_name)
if not bucket.find(bucket_name):
    bucket.create(bucket_name)

now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

# archive the current emr deployment, if present.
response = bucket.list_objects(bucket_name, 'emr')
files = response['files']
for fle in files:
    if not fle['ContentType'] == 'application/x-directory':
        path = fle['Key']
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)

        # move the file to the archive location.
        bucket.copy_object(bucket_name, path, bucket_name, os.path.join('archive', 'emr', now, filename))
        bucket.delete_object(bucket_name, path)

# set identifier, reflecting the checkout folder to build this release.
name = uuid.uuid4().hex

# create an empty folder in tmp
tmp_folder = System.recreate_tmp(name)

# create the bootstrap.sh script.
f = open(os.path.join(tmp_folder, 'bootstrap.sh'), 'wb')
# todo process the dependencies here.
f.write('pip install awscli'.encode('utf-8'))
f.close()

# upload the bootstrap file to aws
bucket.upload(os.path.join(tmp_folder, 'bootstrap.sh'), bucket_name, 'emr/bootstrap/bootstrap.sh')


    # print(file)
    # print(basename(file['Key']))
    # print(os.path.dirname(file['Key']))
    # if not response['ContentType'] == 'application/x-directory':
    #     print(file)

