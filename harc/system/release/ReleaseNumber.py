class ReleaseNumber(object):
    def __init(self):
        object.__init__(self)

    @staticmethod
    def increment_build(release):
        d = release.split(".")
        d[2] = str(int(d[2]) + 1)
        return '.'.join(d)
