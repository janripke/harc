from subprocess import Popen, PIPE
from harc.exceptions.CommandException import CommandException
import json


class Command(object):
    @staticmethod
    def execute(statement):
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise CommandException(error)
        return output

    @staticmethod
    def jsonify(output):
        output = output.rstrip(b'\x1b[0m')
        if output:
            return json.loads(output)
        return output

    @staticmethod
    def stringify(output):
        if output:
            output = output.decode('utf-8')
            output = output.rstrip(chr(13))
            output = output.rstrip(chr(10))
        return output
