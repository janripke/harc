from datetime import datetime
from harc.system.Console import Console


class ConsoleHandler:
    def __init__(self):
        pass

    @staticmethod
    def write(message):
        output = "{0} {1} {2} [{3}.{4}] {5} {6}".format(datetime.now().strftime('%d-%m-%Y %H:%M:%S'), message['logtype_code'], message['job_name'], message['package_name'], message['method_name'], message['message'], message['backtrace'])
        Console.write(output)

