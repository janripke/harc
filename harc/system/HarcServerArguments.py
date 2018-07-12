from harc.system.Arguments import Arguments


class HarcServerArguments(Arguments):
    DEBUG = {"argument": "-d", "type": "int", "help": "debug mode"}
    PORT = {"argument": "-p", "type": "str", "help": "port"}
    BIND = {"argument": "-b", "type": "str", "help": "bind"}

    def __init__(self, description):
        Arguments.__init__(self, description)
        self.add_argument(HarcServerArguments.DEBUG)
        self.add_argument(HarcServerArguments.PORT)
        self.add_argument(HarcServerArguments.BIND)

