import os


class PythonReleaseFile:
    def __init__(self, location, name):
        object.__init__(self)
        self.__location = location
        self.__name = name
        self.__file = None
        self.__quote_char = None

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
        value = None
        self.open()
        lines = self.read()
        for line in lines:
            if '__version__' in line:
                key, value = line.split('=')
                quote_char = self.guess_quote_char(line)
                self.set_quote_char(quote_char)
                value = value.replace(quote_char, "")
        self.close()
        return value

    def set_version(self, version):
        self.open()
        lines = self.read()
        self.close()

        results = []
        for line in lines:
            if '__version__' in line:
                quote_char = self.get_quote_char()
                results.append("__version__ = " + quote_char + version + quote_char)
            else:
                results.append(line)

        self.open('w')
        self.write(chr(10).join(results))
        self.close()

    def set_quote_char(self, quote_char):
        self.__quote_char = quote_char

    def get_quote_char(self):
        return self.__quote_char

    def guess_quote_char(self, line):
        single_count = line.count("'")
        double_count = line.count('"')
        if single_count > 0 and single_count > double_count:
            return "'"
        if double_count > 0 and double_count > single_count:
            return '"'
        return '"'
