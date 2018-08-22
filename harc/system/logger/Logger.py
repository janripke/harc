import inspect
import json
import os


class Logger(object):

    LOG_HANDLERS = "application.log.handlers"
    LOG_DATASOURCE = "application.log.datasource"
    LOG_LEVEL = "application.log.level"

    def __init__(self, parent, filename="log.json"):
        object.__init__(self)
        self.__parent = parent
        self.__settings = self.load_settings(filename)
        self.__levels = {"trace": 0, "debug": 1, "info": 2, "warn": 3, "fatal": 4}
        self.__handlers = self.load_handlers()

    def get_settings(self):
        return self.__settings

    def load_settings(self, filename):
        try:
            handle = open(filename)
            settings = json.load(handle)
            handle.close()
            return settings
        except:
            return {Logger.LOG_HANDLERS: "console"}

    def load_handlers(self):
        settings = self.get_settings()
        handlers = settings[Logger.LOG_HANDLERS]
        handlers = handlers.split(';')
        result = []
        for handler in handlers:
            if handler == 'console':
                from harc.system.logger.ConsoleHandler import ConsoleHandler
                result.append(ConsoleHandler)
            if handler == 'database':
                from harc.system.logger.DatabaseHandler import DatabaseHandler
                datasource = settings[Logger.LOG_DATASOURCE]
                result.append(DatabaseHandler(datasource))
            if handler == 'syslog':
                from harc.system.logger.SyslogHandler import SyslogHandler
                result.append(SyslogHandler)
        return result

    def get_handlers(self):
        return self.__handlers

    def get_levels(self):
        return self.__levels

    def get_parent(self):
        return self.__parent

    def insert(self, message):
        handlers = self.get_handlers()
        for handler in handlers:
            handler.write(message)

    def trace(self, job_name, message, backtrace=''):
        settings = self.get_settings()

        # todo, what about a default value
        log_level = settings[Logger.LOG_LEVEL]
        levels = self.get_levels()
        if levels[log_level] <= levels['trace']:
            parent = self.get_parent()
            package_name = parent.__class__.__name__
            method_name = inspect.stack()[1][3]

            message = {"job_name": job_name, "logtype_code": "trace", "message": message, "package_name": package_name, "method_name": method_name, "backtrace": backtrace}
            self.insert(message)

    def debug(self, job_name, message, backtrace=''):
        settings = self.get_settings()

        # todo, what about a default value
        log_level = settings[Logger.LOG_LEVEL]
        levels = self.get_levels()
        if levels[log_level] <= levels['debug']:
            parent = self.get_parent()
            package_name = parent.__class__.__name__
            method_name = inspect.stack()[1][3]

            message = {"job_name": job_name, "logtype_code": "debug", "message": message, "package_name": package_name, "method_name": method_name, "backtrace": backtrace}
            self.insert(message)

    def info(self, job_name, message, backtrace=''):
        settings = self.get_settings()

        # todo, what about a default value
        log_level = settings[Logger.LOG_LEVEL]
        levels = self.get_levels()
        if levels[log_level] <= levels['info']:
            parent = self.get_parent()
            package_name = parent.__class__.__name__
            method_name = inspect.stack()[1][3]

            message = {"job_name": job_name, "logtype_code": "info", "message": message, "package_name": package_name, "method_name": method_name, "backtrace": backtrace}
            self.insert(message)

    def warn(self, job_name, message, backtrace=''):
        settings = self.get_settings()

        # todo, what about a default value
        log_level = settings[Logger.LOG_LEVEL]
        levels = self.get_levels()
        if levels[log_level] <= levels['warn']:
            parent = self.get_parent()
            package_name = parent.__class__.__name__
            method_name = inspect.stack()[1][3]

            message = {"job_name": job_name, "logtype_code": "warn", "message": message, "package_name": package_name, "method_name": method_name, "backtrace": backtrace}
            self.insert(message)

    def fatal(self, job_name, message, backtrace=''):
        settings = self.get_settings()

        # todo, what about a default value
        log_level = settings[Logger.LOG_LEVEL]
        levels = self.get_levels()
        if levels[log_level] <= levels['fatal']:
            parent = self.get_parent()
            package_name = parent.__class__.__name__
            method_name = inspect.stack()[1][3]

            message = {"job_name": job_name, "logtype_code": "fatal", "message": message, "package_name": package_name, "method_name": method_name, "backtrace": backtrace}
            self.insert(message)