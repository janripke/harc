from threading import Lock
from harc.system.Ora import Ora


class Threads(object):
    def __init__(self, abort):
        object.__init__(self)
        self.__lock = Lock()
        self.__threads = []
        self.__abort = abort
        self.__id = 0

    def get_threads(self):
        return self.__threads

    def set_threads(self, threads):
        self.__threads = threads

    def get_lock(self):
        return self.__lock

    def get_abort(self):
        return self.__abort

    def append(self, t):
        lock = self.get_lock()
        lock.acquire()
        threads = self.get_threads()
        t['name'] = t['thread'].__class__

        if not t.has_key('id'):
            t['id'] = self.next_id()

        if not t.has_key('group'):
            t['group'] = None

        threads.append(t)
        lock.release()

    def has_group(self, group):
        lock = self.get_lock()
        lock.acquire()
        result = False
        threads = self.get_threads()
        for thread in threads:
            if Ora.nvl(thread['group'], '-1') == group:
                result = True
        lock.release()
        return result

    def list_by_group(self, group):
        lock = self.get_lock()
        lock.acquire()
        threads = self.get_threads()
        results = []
        for thread in threads:
            if Ora.nvl(thread['group'], '-1') == group:
                results.append(thread)
        lock.release()
        return results

    def remove_by_group(self, group):
        lock = self.get_lock()
        lock.acquire()
        threads = self.get_threads()
        results = []
        for thread in threads:
            if Ora.nvl(thread['group'], '-1') != group:
                results.append(thread)
        self.set_threads(results)
        lock.release()

    def terminate_by_group(self, group):
        lock = self.get_lock()
        lock.acquire()
        threads = self.get_threads()
        for thread in threads:
            if Ora.nvl(thread['group'], '-1') == group:
                t = thread['thread']
                if t.is_alive():
                    t.terminate()
        lock.release()

    def terminate(self):
        threads = self.get_threads()
        for thread in threads:
            t = thread['thread']
            if str(type(t)) == "<class 'multiprocessing.process.Process'>":
                t.terminate()
                t.join()

    def abort(self):
        threads = self.get_threads()
        abort = self.get_abort()
        abort.aborted(True)
        for thread in threads:
            t = thread['thread']
            if str(type(t)) == "<class 'threading.Thread'>":
                t.join()

    def next_id(self):
        id = self.__id
        id += 1
        self.__id = id
        return id
