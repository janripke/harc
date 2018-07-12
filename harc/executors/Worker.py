class Worker(object):
    def __init__(self, id, settings, claim, abort):
        object.__init__(self)
        self.__id = id
        self.__settings = settings
        self.__claim = claim
        self.__abort = abort
        self.__running = True

    def get_id(self):
        return self.__id

    def get_settings(self):
        return self.__settings

    def get_claim(self):
        return self.__claim

    def get_abort(self):
        return self.__abort

    def is_running(self):
        return self.__running

    def running(self, running):
        self.__running = running
