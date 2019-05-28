import logging
import json
import logging.config
from logging.config import dictConfig


class LogConfig:
    @staticmethod
    def load(path, name=None):
        f = open(path)
        settings = json.load(f)
        f.close()

        dictConfig(settings)
        if name:
            logging.root.name = name


