from flask_restful import Resource
from flask import request
from harc.system.Traceback import Traceback
from harc.system.Settings import Settings
from harc.system.Pip import Pip
from harc.system.System import System
from harc.system.VirtualEnv import VirtualEnv
from harc.system.Ps import Ps
import json
import uuid
import os


class Deploy(Resource):
    def post(self):
        try:
            message = request.get_json(silent=True)
            version = message.get('version')

            # retrieve the settings, containing the projects to deploy.
            data = open("harc.json")
            settings = json.load(data)

            # retrieve the project to deploy.
            project = Settings.find_project(settings, message['project'])
            print "project", project
            if not project:
                message = "project urg not found."
                response = dict()
                response['status'] = 404
                response['message'] = message
                return response

            # kill the daemon process, reflecting the server
            daemon_name = project.get('daemon')
            if Ps.is_active(daemon_name):
                Ps.kill(daemon_name)

            # set identifier, reflecting the checkout folder to build this release.
            name = uuid.uuid4().hex

            # create an empty folder in tmp
            tmp_folder = System.create_tmp(name)

            print tmp_folder
            virtualenv = os.path.join(tmp_folder, 'env')
            response = VirtualEnv.create(virtualenv)
            print response

            response = Pip.install_virtualenv(virtualenv, project['repository'], version, project['name'])
            print response

            response = Ps.start(virtualenv, daemon_name)
            print response

            # change to the working directory of the project.
            # stop the system service
            # remove the virtual environment
            # install the project into the virtual environment
            # start the system service

            response = dict()
            response['status'] = 200
            return response
        except:
            response = Traceback.build()
            response['status'] = 500
            return response

