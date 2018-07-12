from threading import Lock


class Stop(object):
    def __init__(self):
        object.__init__(self)
        self.__lock = Lock()
        self.__stopped = False

    def get_lock(self):
        return self.__lock

    def stopped(self, stopped):
        lock = self.get_lock()
        lock.acquire()
        self.__stopped = stopped
        lock.release()

    def is_stopped(self):
        lock = self.get_lock()
        lock.acquire()
        result = self.__stopped
        lock.release()
        return result
