from threading import Lock


class Claim(object):
    def __init__(self):
        object.__init__(self)
        self.__lock = Lock()

    def get_lock(self):
        return self.__lock

    def acquire(self):
        lock = self.get_lock()
        lock.acquire()

    def release(self):
        lock = self.get_lock()
        lock.release()