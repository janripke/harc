import syslog


class Level:
    def __init__(self):
        pass

    @staticmethod
    def build(logtype_code):
        if logtype_code == 'trace':
            return syslog.LOG_DEBUG
        if logtype_code == 'debug':
            return syslog.LOG_DEBUG
        if logtype_code == 'info':
            return syslog.LOG_INFO
        if logtype_code == 'warn':
            return syslog.LOG_WARNING
        if logtype_code == 'fatal':
            return syslog.LOG_ERR


class SyslogHandler:
    def __init__(self):
        pass

    @staticmethod
    def write(message):
        output = "{0} {1} [{2}.{3}] {4} {5}".format(message['logtype_code'], message['job_name'], message['package_name'], message['method_name'], message['message'], message['backtrace'])
        syslog.syslog(Level.build(message['logtype_code']), output)