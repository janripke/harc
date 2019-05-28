#!/usr/bin/env python
from harc.plugins.Plugable import Plugable


class Plugin(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        self.__command = None

    def get_command(self):
        return self.__command

    def set_command(self, command):
        self.__command = command
