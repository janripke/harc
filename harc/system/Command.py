from subprocess import Popen, PIPE


class Command(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def execute(statement):
        p = Popen([statement], stdout=PIPE, shell=True)
        return p.communicate()[0]
