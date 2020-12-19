class ReleaseFileFactory:
    @staticmethod
    def create(location, name, technology):
        if technology == 'python':
            from harc.system.release.python_release_file import PythonReleaseFile
            return PythonReleaseFile(location, name)
