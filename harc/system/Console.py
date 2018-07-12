import sys


class Console:
    def __init__(self):
        pass

    @staticmethod
    def write(*args):
        count = len(args)
        result = ''
        for i in xrange(count):
            result = result + args[i] + ' '
        result.rstrip(' ')
        sys.stdout.write(result + '\n')
