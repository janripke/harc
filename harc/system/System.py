import shutil
import tempfile
import os
import shutil
import errno


class System(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def create_tmp(folder_name, sub_folder_name=None):
        folder = os.path.join(tempfile.gettempdir(), folder_name)
        if sub_folder_name:
            folder = os.path.join(folder, sub_folder_name)

        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)
        return folder

    @staticmethod
    def copy(src, dest):
        try:
            shutil.copytree(src, dest)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest)
            else:
                print('Directory not copied. Error: %s' % e)
