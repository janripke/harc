from threading import Lock
from harc.system.System import System
import uuid
import os


class Sequence(object):
    def __init__(self, identifier = None):
        object.__init__(self)
        self.__lock = Lock()

        if not identifier:
            identifier = uuid.uuid4().hex

        self.__identfifier = identifier

    def get_lock(self):
        return self.__lock

    def get_identfier(self):
        return self.__identfifier

    def next(self, name):
        lock = self.get_lock()
        lock.acquire()

        identifier = self.get_identfier()
        # set identifier, reflecting the checkout folder to build this release.

        # create an empty folder in tmp
        tmp_folder = System.create_tmp(name)

        path = os.path.join(tmp_folder, identifier)

        # create the sequence if the file is not present.
        if not os.path.isfile(path):
            f = open(path, 'wb')
            f.write(str(0).encode('utf-8'))
            f.flush()
            f.close()

        # open the sequence file and read the current value
        f = open(path, 'rb')
        result = int(f.read())
        result += 1
        f.close()

        f = open(path, 'wb')
        f.write(str(result).encode('utf-8'))
        f.flush()
        f.close()

        lock.release()
        return result