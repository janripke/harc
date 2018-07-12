import shutil
import tempfile
import os


class System(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def create_tmp(project_name):
        folder = tempfile.gettempdir() + os.sep + project_name
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)
        return folder

