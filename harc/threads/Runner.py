import threading


class Runner:
    def __init__(self):
        pass

    @staticmethod
    def run(launcher, *args):
        t = threading.Thread(target=launcher.run, args=args, name=launcher.__class__)
        t.setDaemon(True)
        t.start()
        return t
