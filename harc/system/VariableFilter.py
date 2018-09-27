class VariableFilter:
    def __init__(self):
        pass

    @staticmethod
    def filter(source, arguments):
        result = dict()
        for argument in arguments:
            if source.get(argument):
                result[argument] = source.get(argument)
        return result
