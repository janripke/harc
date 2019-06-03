class File:
    def __init__(self, path):
        self.__path = path

    def get_path(self):
        return self.__path

    def read_lines(self, encoding='utf8'):
        path = self.get_path()
        f = open(path, 'rb')
        lines = f.readlines()
        f.close()

        results = list()
        for line in lines:
            line = line.decode(encoding).replace(chr(10), '')
            results.append(line)
        return results

    def write_lines(self, lines, encoding='utf8'):
        path = self.get_path()
        f = open(path, 'wb')
        for line in lines:
            line = line + chr(10)
            line = line.encode(encoding)
            f.write(line)
        f.close()