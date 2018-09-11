from harc.amazon.AwsBucket import AwsBucket
from datetime import datetime
import os


class Toolbox:
    def __init__(self):
        pass

    @staticmethod
    def archive(profile_name, region_name, bucket_name, sub_folder=''):

        # retrieve the amazon bucket client.
        bucket = AwsBucket(profile_name, region_name)

        # archive the current emr deployment, if present.
        now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        response = bucket.list_objects(bucket_name, sub_folder)
        files = response['files']
        for file in files:
            if not file['ContentType'] == 'application/x-directory':
                path = file['Key']

                # move the file to the archive location.
                bucket.copy_object(bucket_name, path, bucket_name, os.path.join('archive', sub_folder, now, path))
                bucket.delete_object(bucket_name, path)
