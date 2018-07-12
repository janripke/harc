from flask import Flask
from flask_restful import Api
from harc.rest.Job import Job
from harc.rest.Login import Login
from harc.rest.Status import Status
from harc.rest.Deploy import Deploy

import harc
import argparse

app = Flask(__name__)
api = Api(app)

api.add_resource(Login, '/login')
api.add_resource(Job, '/job')
api.add_resource(Status, '/status')
api.add_resource(Deploy, '/deploy')


def main(args=None):
    # Instantiate the parser
    parser = argparse.ArgumentParser(description="harc = Hit And Release Code, probably python.")
    parser.add_argument('-v', action='store_true', help='show the version')
    parser.add_argument('-d', action='store_true', help='debug mode')
    parser.add_argument('-b', type=str, default='127.0.0.1', help='host')
    parser.add_argument('-p', type=int, default='5000', help='port')
    args = parser.parse_args(args)

    if args.v:
        print "tripolis rest server version " + harc.__version__
        exit(0)

    debug = False
    if args.d:
        debug = True

    host = None
    if args.b:
        host = args.b

    port = None
    if args.p:
        port = args.p

    app.run(debug=debug, port=port, host=host)


if __name__ == '__main__':
    main(args=None)

# todo: start parameters, start to listen on a different port, and address
