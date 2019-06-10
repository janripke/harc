class PropertyHelper:

    @staticmethod
    def find_environment(properties, environment):
        environments = properties['environments']
        for env in environments:
            if env['name'] == environment:
                return env

    @staticmethod
    def find_resource_group(properties, environment):
        env = PropertyHelper.find_environment(properties, environment)
        return env.get('resource_group')

    @staticmethod
    def find_key_vault(properties, environment, default_value=None):
        env = PropertyHelper.find_environment(properties, environment)
        key_vault = env.get('key_vault')
        if key_vault is None:
            if default_value is not None:
                key_vault = default_value
        return key_vault

    @staticmethod
    def find_container(properties, environment):
        env = PropertyHelper.find_environment(properties, environment)
        return env.get('container')

    @staticmethod
    def find_platform(properties, environment, default_value=None):
        env = PropertyHelper.find_environment(properties, environment)
        platform = env.get('platform')
        if platform is None:
            if default_value is not None:
                platform = default_value
        return platform
