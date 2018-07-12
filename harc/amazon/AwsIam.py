import boto3


class AwsIam:
    def __init__(self, session=boto3):
        self.__client = session.client('iam')

    def get_client(self):
        return self.__client

    def list_roles(self):
        client = self.get_client()
        response = client.list_roles()
        return response['Roles']

    def find_role(self, name):
        roles = self.list_roles()
        for role in roles:
            if role['RoleName'] == name:
                return role
        return None

    def get_role(self, name):
        client = self.get_client()
        response = client.get_role(RoleName=name)
        return response['Role']

    def create_role(self, name, assume_role_policy_document):
        client = self.get_client()
        response = client.create_role(RoleName=name, AssumeRolePolicyDocument=assume_role_policy_document)
        return response

    def delete_role(self, name):
        client = self.get_client()
        response = client.delete_role(
            RoleName=name
        )
        return response

    def attach_role_policy(self, role_name, policy_arn):
        client = self.get_client()
        response = client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        return response

    def detach_role_policy(self, role_name, policy_arn):
        client = self.get_client()
        response = client.detach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        return response

    def list_role_policies(self, role_name):
        client = self.get_client()
        response = client.list_role_policies(
            RoleName=role_name
        )
        return response
