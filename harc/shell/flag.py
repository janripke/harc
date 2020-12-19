class Flag(object):
    @staticmethod
    def format(option, value):
        if value:
            return "{}".format(option)
        return ''
