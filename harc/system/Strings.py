class Strings:
    def __init__(self):
        pass

    @staticmethod
    def concat(*args):
        count = len(args)
        result = ""
        for i in xrange(count):
            result = result + args[i] + ' '
        result.rstrip(' ')
        return result

    @staticmethod
    def encode(value, encoding):
        if value:
            return value.encode(encoding)
        return value

    @staticmethod
    def split_index(s, key):
        count = len(s)
        result = []
        for i in xrange(0, count):
            if s[i] == key:
                result.append(i)
        return result

    @staticmethod
    def word(s, index):
        count = len(s)
        result = ''
        for i in xrange(index+1, count):
            if s[i] not in ('abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQWSTUVWXYZ_'):
                return result
            result += s[i]
        return result

    @staticmethod
    def keywords(s, key):
        indexes = Strings.split_index(s, key)
        results = []
        for index in indexes:
            results.append(Strings.word(s, index))
        return results

