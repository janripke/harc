from harc.threading.RuntimeException import RuntimeException


class Runnable(object):
    def __init__(self):
        object.__init__(self)

    def run(self):
        raise RuntimeException("method not implemented")
