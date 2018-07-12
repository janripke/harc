import boto3


class AwsBucket:
    def __init__(self, session=boto3):
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

    def create(self, acl, bucket_name, location):
        client = self.get_client()
        response = client.create_bucket(ACL=acl, Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': location})
        return response

    def upload(self, file, bucket_name, key_name):
        client = self.get_client()
        response = client.upload_fileobj(file, bucket_name, key_name)
        return response

    def copy_object(self, source_bucket, source_key, target_bucket, target_key):
        client = self.get_client()

        response = client.copy_object(
            Bucket=target_bucket,
            CacheControl='string',
            CopySource={'Bucket': source_bucket, 'Key': source_key},
            Key=target_key)
        return response
