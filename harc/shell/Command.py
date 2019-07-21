from subprocess import Popen, PIPE, STDOUT
from harc.exceptions.CommandException import CommandException
import json


class Command(object):
    @staticmethod
    def execute(statement, print_output=False):
        p = Popen([statement], stdout=PIPE, stderr=STDOUT, shell=True)

        output = bytes()
        while True:
            o = p.stdout.readline()
            if o:
                output += o
                # FIXME: should also be possible to redirect output to another IO writer
                if print_output:
                    print(Command.stringify(o).rstrip())
            if p.poll() is not None:
                break
        p.wait()

        if p.returncode != 0:
            raise CommandException("Command '{}' failed with return code {}".format(
                statement, p.returncode), p.returncode, output)
        return output

    # OLD METHOD
    # @staticmethod
    # def execute(statement):
    #     p = Popen([statement], stdout=PIPE, stderr=PIPE, shell=True)
    #     output, error = p.communicate()
    #     if p.returncode != 0:
    #         raise CommandException(error)
    #     return output

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
