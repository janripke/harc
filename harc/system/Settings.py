class Settings(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def find_project(settings, project_name):
        projects = settings['projects']
        for project in projects:
            if project['name'] == project_name:
                return project

    # @staticmethod
    # def list_lambdas(settings, project_name):
    #     project = Settings.find_project(settings, project_name)
    #     lambdas = project['lambdas']
    #     return lambdas
    #
    # @staticmethod
    # def find_lambda(settings, project_name, lambda_name):
    #     lambdas = Settings.list_lambdas(settings, project_name)
    #     for la in lambdas:
    #         if lambda_name in la.keys():
    #             return la[lambda_name]

    @staticmethod
    def list_dependencies(settings, project_name, lambda_name):
        project = Settings.find_project(settings, project_name)
        dependencies = project['dependencies']
        return dependencies.get(lambda_name, [])


        la = Settings.find_lambda(settings, project_name, lambda_name)
        print("lambda", la)
        dependencies = la['dependencies']
        return dependencies

    @staticmethod
    def find_detail(settings, project_name, environment):
        details = settings[environment]
        for detail in details:
            if detail['name'] == project_name:
                return detail

    @staticmethod
    def find_environment(settings, environment):
        return settings[environment]

    @staticmethod
    def find_aws_profile_name(settings, environment):
        env = Settings.find_environment(settings, environment)
        return env['aws_profile_name']

    @staticmethod
    def find_aws_bucket_name(settings, environment):
        env = Settings.find_environment(settings, environment)
        return env['aws_bucket_name']

    @staticmethod
    def find_aws_region_name(settings, environment):
        env = Settings.find_environment(settings, environment)
        return env['aws_region_name']
