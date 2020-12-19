import logging
import logging.config
import tempfile
import os
import shutil
import errno
import json

from logging.config import dictConfig
from pathlib import Path

import harc

FILE_NOT_FOUND = "File '{}' not found."


def load_logger(filename, name=None):
    path = lookup(filename)

    with open(path) as fp:
        settings = json.load(fp)

        dictConfig(settings)
        if name:
            logging.root.name = name


def lookup(*filename):
    """
    Return a the absolute path of the given filename, after looking in the current folder,
    the package folder, the .harc folder located in the home folder or
    the path the filename itself points to

    :param filename:
    :return:
    """

    url = Path.joinpath(Path(), *filename)
    if url.is_file():
        return str(url)

    url = Path.joinpath(Path(os.path.dirname(harc.__file__)), *filename)
    if url.is_file():
        return str(url)

    url = Path.joinpath(Path.home(), '.harc', *filename)
    if url.is_file():
        return str(url)

    url = Path.joinpath(Path(*filename))
    if url.is_file():
        return str(url)

    raise FileNotFoundError(FILE_NOT_FOUND.format(str(*filename)))


def load_json(*filename):
    path = lookup(*filename)
    with open(path) as fp:
        properties = json.load(fp)
        return properties


def create_tmp(folder_name, sub_folder_name=None):
    folder = os.path.join(tempfile.gettempdir(), folder_name)
    if sub_folder_name:
        folder = os.path.join(folder, sub_folder_name)

    if not os.path.isdir(folder):
        os.mkdir(folder)
    return folder


def recreate_tmp(folder_name, sub_folder_name=None):
    folder = os.path.join(tempfile.gettempdir(), folder_name)
    if sub_folder_name:
        folder = os.path.join(folder, sub_folder_name)

    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
    return folder


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)
