class ExpressionParser:
    def __init__(self):
        pass

    @staticmethod
    def parse(stream, expressions):
        for expression in expressions:
            if expressions[expression]:
                stream = stream.replace("{{"+expression+"}}", expressions[expression])
        return stream
