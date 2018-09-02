import boto3


class AwsLambda:
    def __init__(self, profile_name='default', region_name='eu-west-1'):
        session = boto3.Session(profile_name=profile_name, region_name=region_name)
        self.__client = session.client('lambda')

    def get_client(self):
        return self.__client

    def list_functions(self):
        client = self.get_client()
        response = client.list_functions()
        return response['Functions']

    def find_function(self, name):
        functions = self.list_functions()
        for function in functions:
            if function['FunctionName'] == name:
                return function
        return None

    def create_function(self, name, role, handler, code, description, publish=True, vpc_config=None):
        client = self.get_client()
        response = client.create_function(
            FunctionName=name,
            Code=code,
            Runtime='python2.7',
            Role=role,
            Handler=handler,
            Description=description,
            Publish=publish,
            VpcConfig=vpc_config)
        return response

    def update_function_code(self, name, code, publish=True, dry_run=False):
        client = self.get_client()
        response = client.update_function_code(
            FunctionName=name,
            S3Bucket=code['S3Bucket'],
            S3Key=code['S3Key'],
            Publish=publish,
            DryRun=dry_run
        )
        return response

    def delete_function(self, name):
        client = self.get_client()
        response = client.delete_function(
            FunctionName=name
        )
        return response
