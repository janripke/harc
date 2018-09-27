import json
settings = dict()


class VariableFilter:
    def __init__(self):
        pass

    @staticmethod
    def filter(source, arguments):
        result = dict()
        for argument in arguments:
            if source.get(argument):
                result[argument] = source.get(argument)
        return result


class ExpressionParser:
    def __init__(self):
        pass

    @staticmethod
    def parse(stream, expressions):
        for expression in expressions:
            if expressions[expression]:
                stream = stream.replace("{{"+expression+"}}", expressions[expression])
        return stream


e = dict()
e['name_pattern'] = '{{basename}}-{{environment}}'
e['aws_profile_name'] = 'default'
e['deploy_bucket_name'] = 'elsevier-mdp-dev-deploy'
e['aws_region_name'] = 'eu-west-1'
settings['sandbox'] = e


sandbox = settings.get('sandbox')
name_pattern = sandbox.get('name_pattern')


basename = 'register'
environment = 'sandbox'


maps = VariableFilter.filter(locals(), ['basename', 'environment'])
print(maps)
basename = ExpressionParser.parse(name_pattern, maps)
print(basename)
# result = json.loads(result)

# print(result)