class ConsumeException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return repr(self.__message)

    def get_message(self):
        return self.__message
