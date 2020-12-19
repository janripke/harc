class Key:
    @staticmethod
    def format(key, value):
        if value:
            return "{}={}".format(key, value)
        return ''


class SpaceSeparatedKeys:
    @staticmethod
    def format(option, value):
        if value:
            result = ''
            keys = value.keys()
            for key in keys:
                result = result + "'{}={}' ".format(key, value[key])
            result = result.rstrip(' ')
            return "{} {}".format(option, result)
        return ''
