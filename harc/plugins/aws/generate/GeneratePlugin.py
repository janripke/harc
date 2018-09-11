from harc.plugins.Plugable import Plugable
from harc.system.Ora import Ora
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
    def create_file(template_dir, template_filename, path, filename, attributes):
        # create setup.py
        template_setup = os.path.join(template_dir, template_filename)
        f = open(template_setup)
        stream = f.read()
        f.close()

        keys = attributes.keys()
        for key in keys:
            stream = stream.replace(key, attributes[key])

        setup = os.path.join(path, filename)
        f = open(setup, 'w')
        f.write(stream)
        f.close()

    @staticmethod
    def execute(arguments, settings, properties):
        template_dir = os.path.join(properties.get('plugin.dir'), 'aws', 'generate', 'templates')
        print(template_dir)

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

        Generate.fail_on_project_exists(project_dir)

        # create the project folder
        os.mkdir(project_dir)
        print(os.path.exists(project_dir))

        # create the module, reflecting the base of the project.
        # todo: if the project contains a - in the replace it with a _
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

        # create setup.py
        Generate.create_file(template_dir, 'setup.py', project_dir, 'setup.py', attributes)

        # create harc.json
        Generate.create_file(template_dir, 'harc.json', project_dir, 'harc.json', attributes)

        # create __init__.py
        Generate.create_file(template_dir, '__init__.py', module_dir, '__init__.py', attributes)

        # create LICENSE
        Generate.create_file(template_dir, 'LICENSE', project_dir, 'LICENSE', attributes)

        # create MANIFEST.in
        Generate.create_file(template_dir, 'MANIFEST.in', project_dir, 'MANIFEST.in', attributes)

        # create setup.cfg
        Generate.create_file(template_dir, 'setup.cfg', project_dir, 'setup.cfg', attributes)

        # create README.md
        Generate.create_file(template_dir, 'README.md', project_dir, 'README.md', attributes)

        # create acme.py
        lambdas_dir = os.path.join(module_dir, 'lambdas')
        os.mkdir(lambdas_dir)

        Generate.create_file(template_dir, 'lambda.py', lambdas_dir, 'acme.py', attributes)

        init = os.path.join(lambdas_dir, '__init__.py')
        f = open(init, 'w')
        f.write('')
        f.close()

        # create Event.py
        system_dir = os.path.join(module_dir, 'system')
        os.mkdir(system_dir)

        Generate.create_file(template_dir, 'Event.py', system_dir, 'Event.py', attributes)

        init = os.path.join(system_dir, '__init__.py')
        f = open(init, 'w')
        f.write('')
        f.close()
