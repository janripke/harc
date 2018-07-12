import inspect
import json
import os
import argparse
from flask import request
from flask_restful import Resource
from flask_restful import abort
from harc.system.logger.Logger import Logger
from harc.system.Traceback import Traceback
from harc.system.Command import Command
from harc.connectors.DatasourceBuilder import DatasourceBuilder
from harc.repositories.CommandRepository import CommandRepository
from harc.repositories.SessionRepository import SessionRepository
from harc.plugins.PluginFactory import PluginFactory
from harc.system.HarcCliArguments import HarcCliArguments
from harc.repositories.JobRepository import JobRepository
from harc.messaging.Message import Message
from harc.repositories.LogRepository import LogRepository


class Status(Resource):
    def post(self):
        logger = Logger(self)
        job_name = ''
        try:
            harc = DatasourceBuilder.build("harc-ds.json")
            content = request.get_json(silent=True)
            logger.info(job_name, json.dumps(content))
            session = content['session']

            session_repository = SessionRepository(harc)
            if not session_repository.valid(session):
                abort(403, message='failed', reason='session not found', job_name=job_name)

            job_name = content['job_name']
            log_repository = LogRepository(harc)
            logs = log_repository.list_by_job_name(job_name)
            return logs

        except:
            result = Traceback.build()
            logger.fatal('', result['message'], result['backtrace'])
            abort(500, message='failed', reason=result['message'], backtrace=result['backtrace'], job_name=job_name)





    # def post(self):
    #     logger = Logger(self)
    #     job_name = ''
    #     try:
    #         harc = DatasourceBuilder.build("harc-ds.json")
    #         job_repository = JobRepository(harc)
    #         job = job_repository.job()
    #         job_name = job['job_name']
    #
    #         content = request.get_json(silent=True)
    #         logger.info("", json.dumps(content))
    #         session = content['session']
    #
    #         session_repository = SessionRepository(harc)
    #         if not session_repository.valid(session):
    #             abort(403, message='failed', reason='session not found', job_name=job_name)
    #
    #         parser = HarcCliArguments("Harc, hit and release code")
    #         args = parser.parse_content(content)
    #
    #         os.path.abspath('.')
    #
    #         data = open("harc.json")
    #         settings = json.load(data)
    #
    #         properties = {}
    #         properties['harc_dir'] = os.path.abspath('.')
    #         properties['job_name'] = job_name
    #         plugin = PluginFactory.create_plugin(args.command)
    #
    #         path, filename = os.path.split(inspect.getfile(plugin))
    #         properties['plugin_dir'] = path
    #
    #         plugin.execute(args, settings, properties)
    #
    #         return {"message": "success", "job_name": job_name}
    #
    #     except:
    #         result = Traceback.build()
    #         logger.fatal('', result['message'], result['backtrace'])
    #         abort(500, message='failed', reason=result['message'], backtrace=result['backtrace'], job_name=job_name)
