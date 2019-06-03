class PropertyHelper:

    @staticmethod
    def find_resource_group(properties, environment):
        environments = properties['environments']
        for env in environments:
            if env['name'] == environment:
                return env.get('resource_group')

    @staticmethod
    def find_container(properties, environment):
        environments = properties['environments']
        for env in environments:
            if env['name'] == environment:
                return env.get('container')