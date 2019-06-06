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
    def find_key_vault(properties, environment):
        env = PropertyHelper.find_environment(properties, environment)
        return env.get('key_vault')

    @staticmethod
    def find_container(properties, environment):
        env = PropertyHelper.find_environment(properties, environment)
        return env.get('container')