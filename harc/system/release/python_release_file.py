import os


class PythonReleaseFile:
    def __init__(self, location, name):
        object.__init__(self)
        self.__location = location
        self.__name = name
        self.__file = None

    def get_location(self):
        return self.__location

    def get_name(self):
        return self.__name

    def open(self, mode='r'):
        location = self.get_location()
        name = self.get_name()
        self.__file = open(os.path.join(location, name, "__init__.py"), mode=mode)

    def read(self):
        stream = self.__file.read()
        stream = stream.replace(chr(13) + chr(10), chr(10))
        stream = stream.replace(chr(13), chr(10))
        return stream.split(chr(10))

    def write(self, stream):
        self.__file.write(stream)

    def close(self):
        self.__file.close()

    def get_version(self):
        result = None
        self.open()
        lines = self.read()
        for line in lines:
            if '__version__' in line:
                result = line.strip("__version__ ='")
        self.close()
        return result

    def set_version(self, version):
        self.open()
        lines = self.read()
        self.close()

        results = []
        for line in lines:
            if '__version__' in line:
                results.append("__version__ = '" + version + "'")
            else:
                results.append(line)

        self.open('w')
        self.write(chr(10).join(results))
        self.close()