import shutil
import uuid
import os
import logging

from harc.plugins.Plugable import Plugable
from harc.system.io.Files import Files
from urllib.parse import urlparse, quote
import click
from harc.system.Git import Git
from harc.system.System import System
from harc.system.Docker import Docker
from harc.system.io.File import File
from harc.system.Requirements import Requirements
from harc.system.PropertyHelper import PropertyHelper
from harc.plugins.UsernameOption import UsernameOption
from harc.plugins.PasswordOption import PasswordOption
from harc.plugins.EnvironmentOption import EnvironmentOption
from harc.shell.key import Key


class DPythonGenerate:
    @click.command()
    @click.argument('project')
    @click.argument('module')
    def test_Asmi(project, module,*dict1):
        print('in execute method')

        # logger.debug("username : {}, version: {}, environment : {}".format(username, version, environment))

        # create the attribute list, containing the words to parse.
        attributes = dict()
        attributes['{{File1}}'] = 'requirements.txt'
        attributes['{{File2}}'] = 'harc.json'
        attributes['{{File3}}'] = 'LICENSE'
        attributes['{{File4}}'] = 'MANIFEST.in'
        attributes['{{File5}}'] = 'setup.cfg'
        current_dir = dict1.__getattribute__('current.dir')
      # retrieve the properties, set by the cli

    # properties = self.obj
    #  cbca_api_dir = os.path.join(properties.get('cbca_api.dir'))
    # current_dir = properties.get('current.dir')

    #        project_dir = os.path.join(current_dir, project)
    #       DPythonGenerate.fail_on_project_exists(project_dir)
    #      os.mkdir(project_dir)
    # module = project
    #     repo_dir = os.path.join(project_dir, module)
    #    DPythonGenerate.fail_on_project_exists(repo_dir)
    #   os.mkdir(repo_dir)
    # need to implement for loop for rest of the files
    # src = os.path.join(cbca_api_dir, 'Requirements.txt')
    #  dst = repo_dir
    # if not os.path.isfile('/repo_dir/requirements.txt'):
    # shutil.copy(src, dst)

    # DPythonGenerate.parse_file(file, target, attributes)
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
    def fail_on_project_exists(path):
        if os.path.exists(path):
            message = path + " already present"
            raise RuntimeError(message)
