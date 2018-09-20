
import boto3


class AwsBucket:
    def __init__(self, profile_name='default', region_name='eu-west-1'):
        session = boto3.Session(profile_name=profile_name, region_name=region_name)
        self.__client = session.client('s3')

    def get_client(self):
        return self.__client

    def find(self, bucket_name):
        client = self.get_client()
        response = client.list_buckets()
        buckets = response['Buckets']
        for bucket in buckets:
            if bucket['Name'] == bucket_name:
                return bucket
        return None

    def delete(self, bucket_name):
        client = self.get_client()
        response = client.delete_bucket(Bucket=bucket_name)
        return response

    def create(self, bucket_name, acl='private', location='eu-west-1'):
        # todo: Shall we default them to some values? (Already did here)
        # Or should we retrieve location from db?
        client = self.get_client()
        response = client.create_bucket(ACL=acl, Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': location})
        return response

    def get_object(self, bucket_name, key_name):
        client = self.get_client()
        response = client.get_object(
            Bucket=bucket_name,
            Key=key_name
        )
        return response

    def copy_object(self, source_bucket, source_key, target_bucket, target_key, metadata=dict()):
        client = self.get_client()

        response = client.copy_object(
            Bucket=target_bucket,
            CopySource={'Bucket': source_bucket, 'Key': source_key},
            Key=target_key,
            Metadata=metadata,
            MetadataDirective='REPLACE'
        )
        return response

    def upload(self, path, bucket_name, key_name, metadata=dict()):
        # an existing file is overwritten.
        client = self.get_client()

        file = open(path, 'rb')
        client.put_object(
            Bucket=bucket_name,
            Key=key_name,
            Body=file,
            Metadata=metadata
        )
        file.close()

    def download(self, path, bucket_name, key_name):
        # an existing file is overwritten.
        client = self.get_client()

        f = open(path, 'wb')
        client.download_fileobj(bucket_name, key_name, f)
        f.close()
        # with open('filename', 'wb') as data:
        #     s3.download_fileobj('mybucket', 'mykey', data)

    def delete_object(self, bucket_name, key_name):
        # delete a file object, when the file object does not exists, no meaningful error is given.
        # knowing this, this method returns None
        client = self.get_client()

        client.delete_object(
            Bucket=bucket_name,
            Key=key_name,
        )

    def list(self):
        client = self.get_client()
        response = client.list_buckets()
        return response['Buckets']

    def list_objects(self, bucket_name, prefix=''):
        client = self.get_client()

        response = client.list_objects(
            Bucket=bucket_name,
            Prefix=prefix
        )

        result = dict()
        files = response.get('Contents', [])
        result['files'] = files
        result['ResponseMetadata'] = response['ResponseMetadata']
        for file in files:
            response = self.get_object(bucket_name, file.get('Key'))
            file['ContentType'] = response['ContentType']

        return result

    @staticmethod
    def url(bucket_name, key_name):
        url = 's3://{}/{}'.format(bucket_name, key_name)
        return url
