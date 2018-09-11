from harc.system.Arguments import Arguments


class HarcCliArguments(Arguments):
    COMMAND = {"argument": "command", "type": "str", "help": "command"}
    BRANCH = {"argument": "-b", "type": "str", "help": "branch"}
    USERNAME = {"argument": "-u", "type": "str", "help": "username"}
    PASSWORD = {"argument": "-p", "type": "str", "help": "password"}
    VERSION = {"argument": "-v", "type": "str", "help": "version"}
    ENVIRONMENT = {"argument": "-e", "type": "str", "help": "environment"}
    TECHNOLOGY = {"argument": "-t", "type": "str", "help": "technology"}
    FILENAME = {"argument": "-f", "type": "str", "help": "filename"}
    SERVICE = {"argument": "-s", "type": "str", "help": "service"}
    PROJECT = {"argument": "-n", "type": "str", "help": "project"}
    JOB_NAME = {"argument": "-j", "type": "str", "help": "job_name"}

    def __init__(self, description):
        Arguments.__init__(self, description)
        self.add_argument(HarcCliArguments.COMMAND)
        self.add_argument(HarcCliArguments.BRANCH)
        self.add_argument(HarcCliArguments.USERNAME)
        self.add_argument(HarcCliArguments.PASSWORD)
        self.add_argument(HarcCliArguments.VERSION)
        self.add_argument(HarcCliArguments.ENVIRONMENT)
        self.add_argument(HarcCliArguments.TECHNOLOGY)
        self.add_argument(HarcCliArguments.SERVICE)
        self.add_argument(HarcCliArguments.PROJECT)
        self.add_argument(HarcCliArguments.JOB_NAME)
