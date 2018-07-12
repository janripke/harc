

class ReleaseFileFactory(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def create(location, name, technology):
        if technology == 'python':
            from harc.system.release.PythonReleaseFile import PythonReleaseFile
            return PythonReleaseFile(location, name)