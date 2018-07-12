from threading import Lock


class Abort(object):
    def __init__(self):
        object.__init__(self)
        self.__lock = Lock()
        self.__aborted = False

    def get_lock(self):
        return self.__lock

    def aborted(self, aborted):
        lock = self.get_lock()
        lock.acquire()
        self.__aborted = aborted
        lock.release()

    def is_aborted(self):
        lock = self.get_lock()
        lock.acquire()
        result = self.__aborted
        lock.release()
        return result