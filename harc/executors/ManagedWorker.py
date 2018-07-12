from harc.executors.Worker import Worker


class ManagedWorker(Worker):
    def __init__(self, id, settings, claim, abort, stop):
        Worker.__init__(self, id, settings, claim, abort)
        self.__stop = stop

    def get_stop(self):
        return self.__stop
