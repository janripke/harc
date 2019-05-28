class Parameter(object):
    @staticmethod
    def format(option, value):
        if value:
            return "{} '{}'".format(option, value)
        return ''
