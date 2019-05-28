from harc.plugins.Plugable import Plugable
from harc.system.Ora import Ora
from harc.system.io.Files import Files
import os
import os
import json
import shutil


class Generate(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def fail_on_project_exists(path):
        if os.path.exists(path):
            message = path + " already present"
            raise RuntimeError(message)

    @staticmethod
    def parse_file(src, dst, attributes):
        # create load.py
        f = open(src)
        stream = f.read()
        f.close()

        keys = attributes.keys()
        for key in keys:
            stream = stream.replace(key, attributes[key])

        f = open(dst, 'w')
        f.write(stream)
        f.close()

    @staticmethod
    def execute(arguments, settings, properties):
        template_dir = os.path.join(properties.get('plugin.dir'), 'aws', 'generate', 'templates')

        technology = arguments.t
        print(technology)

        # enter the name of the project to generate.
        project = input('project : ')
        description = input('description : ')
        repository = input('repository : ')
        profile = input('aws profile [default]: ')
        profile = Ora.nvl(profile, "default")
        region = input('aws region [eu-west-1]: ')
        region = Ora.nvl(region, "eu-west-1")
        bucket = input('aws deployment bucket : ')

        current_dir = properties.get('current.dir')
        project_dir = os.path.join(current_dir, project)

        # fail when the project already exists
        Generate.fail_on_project_exists(project_dir)

        # create the project folder
        os.mkdir(project_dir)

        # create the module, reflecting the base of the project.
        # todo: if the project contains a - in the project name, replace it with a _
        module = project
        module_dir = os.path.join(project_dir, module)
        os.mkdir(module_dir)

        # create the attribute list, containing the words to parse.
        attributes = dict()
        attributes['{{project}}'] = project
        attributes['{{description}}'] = description
        attributes['{{module}}'] = module
        attributes['{{repository}}'] = repository
        attributes['{{profile}}'] = profile
        attributes['{{region}}'] = region
        attributes['{{bucket}}'] = bucket

        # create and parse the files
        lambda_dir = os.path.join(template_dir, 'lambda')
        files = Files.list(lambda_dir)
        for file in files:
            target = os.path.join(module_dir, file.replace(lambda_dir, '').lstrip(os.sep))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            Generate.parse_file(file, target, attributes)
