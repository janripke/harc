class PluginFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_plugin(command):
        if command == 'git:branches':
            from harc.plugins.GitBranches import GitBranches
            return GitBranches
        if command == 'git:release':
            from harc.plugins.GitRelease import GitRelease
            return GitRelease
        if command == 'aws:eb:deploy':
            from harc.plugins.AwsEbDeploy import AwsEbDeploy
            return AwsEbDeploy
        if command == 'aws:lambda:deploy':
            from harc.plugins.AwsLambdaDeploy import AwsLambdaDeploy
            return AwsLambdaDeploy
        if command == 'aws:emr:deploy':
            from harc.plugins.AwsEmrDeploy import AwsEmrDeploy
            return AwsEmrDeploy
        if command == 'aws:eb:deploy':
            from harc.plugins.AwsEbDeploy import AwsEbDeploy
            return AwsEbDeploy

