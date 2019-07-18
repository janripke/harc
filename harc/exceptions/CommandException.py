class CommandException(Exception):
    def __init__(self, message, retcode, output):
        self.__retcode = retcode
        self.__output = output
        Exception.__init__(self, message)

    def get_retcode(self):
        return self.__retcode

    def get_output(self):
        return self.__output
