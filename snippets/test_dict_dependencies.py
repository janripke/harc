# "dependencies": {
#     "double.py": [
#         {
#             "name": "requests"
#         },
#         {
#             "name": "mdp_toolbox",
#             "version": "1.0.0",
#             "repo": "https://gitlab.et-scm.com/MDP/mdp-toolbox.git"
#         }
#     ],
#     "register.py": [
#         "requests"
#     ]
# }
import json
from harc.system.Settings import Settings
from harc.system.System import System
from harc.system.Pip import Pip
import uuid
from urllib.parse import urlparse, quote
from harc.plugins.PluginException import PluginException

# create the project main part
project = dict()
project['name'] = 'mdp_lambda'
project['technology'] = 'python'
project['repository'] = "https://gitlab.et-scm.com/MDP/mdp-lambda.git"

# create lambdas part
find_lambdas = list()
find_lambdas.append("lambdas")
project['find_lambdas'] = find_lambdas

# create dependency part
module_list = list()

module = dict()
module['name'] = "requests"
module_list.append(module)

module = dict()
module['name'] = "mdp_toolbox"
module['version'] = "1.0.1"
module['repository'] = "https://gitlab.et-scm.com/MDP/mdp-toolbox.git"
module_list.append(module)


dependencies = dict()
dependencies['double.py'] = module_list
dependencies['register.py'] = module_list

project['dependencies'] = dependencies

projects = list()
projects.append(project)

# create the environment part
settings = dict()
settings['projects'] = projects

environment = dict()
environment['aws_profile_name'] = 'default'
environment['aws_bucket_name'] = 'elsevier-mdp-dev-source'
environment['aws_region_name'] = 'eu-west-1'
settings['dev'] = environment

project_name = "mdp_lambda"
filename = "register.py"
username = "ripkej"
password = "*"


build_name = uuid.uuid4().hex
build_folder = System.recreate_tmp(build_name)
print(build_folder)

dependencies = Settings.list_dependencies(settings, project_name, filename)
for dependency in dependencies:
    module_name = dependency['name']
    module_version = dependency.get('version')
    module_repo = dependency.get('repository')

    module = module_name

    if module_version:
        module = module_name + "==" + module_version

    if module_repo:
        module = module_repo
        module_url = urlparse(module_repo)

        if module_url.scheme in ['http', 'https']:
            if not username:
                raise PluginException("no username")

            if not password:
                raise PluginException("no password")

            module = "git+" + module_url.scheme + "://'{0}':'{1}'@" + module_url.netloc + module_url.path
            module = module.format(quote(username), quote(password))

            if module_version:
                module = "git+" + module_url.scheme + "://'{0}':'{1}'@" + module_url.netloc + module_url.path + '@' + module_version + " --upgrade"
                module = module.format(quote(username), quote(password))

    print(module)
    Pip.install(module, build_folder)
