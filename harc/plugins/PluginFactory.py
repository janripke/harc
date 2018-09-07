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
        if command == 'git:deploy':
            from harc.plugins.GitDeploy import GitDeploy
            return GitDeploy
        if command == 'aws:lambda:deploy':
            from harc.plugins.AwsLambdaDeploy import AwsLambdaDeploy
            return AwsLambdaDeploy
        if command == 'aws:emr:deploy':
            from harc.plugins.AwsEmrDeploy import AwsEmrDeploy
            return AwsEmrDeploy
        if command == 'aws:eb:deploy':
            from harc.plugins.AwsEmrDeploy import AwsEbDeploy
            return AwsEbDeploy
        if command == 'http:git:deploy:all':
            from harc.plugins.HttpGitDeployAll import HttpGitDeployAll
            return HttpGitDeployAll
        if command == 'service:start':
            from harc.plugins.StartService import StartService
            return StartService
        if command == 'http:services:start':
            from harc.plugins.HttpStartServices import HttpStartServices
            return HttpStartServices
        if command == 'service:stop':
            from harc.plugins.StopService import StopService
            return StopService
        if command == 'http:services:stop':
            from harc.plugins.HttpStopServices import HttpStopServices
            return HttpStopServices
        if command == 'http:status':
            from harc.plugins.HttpStatus import HttpStatus
            return HttpStatus
        if command == 'oracle:parse':
            from harc.plugins.generate.Generate import Generate
            return Generate
