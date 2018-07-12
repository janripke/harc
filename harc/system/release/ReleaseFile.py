from harc.system.release.ReleaseFileFactory import ReleaseFileFactory


class ReleaseFile(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def get_version(location, name, technology):
        release_file = ReleaseFileFactory.create(location, name, technology)
        return release_file.get_version()

    @staticmethod
    def set_version(location, name, technology, version):
        release_file = ReleaseFileFactory.create(location, name, technology)
        release_file.set_version(version)