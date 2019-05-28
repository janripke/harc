class Key:
    @staticmethod
    def format(key, value):
        if value:
            return "{}={}".format(key, value)
        return ''
