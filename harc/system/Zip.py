from zipfile import ZipFile
from harc.system.io.Files import Files
import os


class Zip:
    def __init__(self):
        pass

    @staticmethod
    def create(zip_file, folder):
        files = Files.list(folder)
        f = ZipFile(zip_file, 'w')
        for file in files:
            f.write(file, file.replace((folder + os.sep), ''))
        f.close()
