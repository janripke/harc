import json
from flask import request
from flask_restful import Resource
from flask_restful import abort
from harc.system.logger.Logger import Logger
from harc.system.Traceback import Traceback
from harc.connectors.DatasourceBuilder import DatasourceBuilder
from harc.repositories.UserRepository import UserRepository


class Login(Resource):

    def post(self):
        logger = Logger(self)
        try:
            content = request.get_json(silent=True)
            logger.trace("", json.dumps(content))

            harc = DatasourceBuilder.build("harc-ds.json")
            user_repository = UserRepository(harc)
            result = user_repository.login(content['username'], content['password'])
            logger.trace("", str(result))

            if not result:
                return {"message": "failed", "reason": "you do not have permission", "backtrace": ""}, 403

            return {"message": "success", "session": result}
        except:
            result = Traceback.build()
            logger.fatal('', result['message'], result['backtrace'])
            abort(500, message='failed', reason=result['message'], backtrace=result['backtrace'])
