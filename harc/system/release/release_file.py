from harc.system.release.release_file_factory import ReleaseFileFactory


def get_version(location, name, technology):
    release_file = ReleaseFileFactory.create(location, name, technology)
    return release_file.get_version()


def set_version(location, name, technology, version):
    release_file = ReleaseFileFactory.create(location, name, technology)
    release_file.set_version(version)
