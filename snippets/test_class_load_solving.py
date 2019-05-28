import os
import harc
import re
from importlib import import_module, invalidate_caches
from pathlib import Path

import inspect



class Pattern:
    """
    returns a match when no pattern is given.
    """
    @staticmethod
    def match(pattern, string):
        if pattern:
            prog = re.compile(pattern, re.IGNORECASE)
            if prog.match(string):
                return True
            return False
        return True


class Dirs:
    @staticmethod
    def list(path, excludes=[], recursive=False):
        results = list()
        elements = os.listdir(path)
        for element in elements:
            node = os.path.join(path, element)
            if os.path.isdir(node) and element not in excludes:
                results.append(node)
            if recursive and os.path.isdir(node):
                results.extend(Dirs.list(node, excludes, recursive))
        return results


class Files:
    @staticmethod
    def list(path, excludes=[], pattern=None):
        results = list()
        elements = os.listdir(path)
        for element in elements:
            node = os.path.join(path, element)
            if os.path.isfile(node) and element not in excludes and Pattern.match(pattern, node):
                results.append(node)
        return results


class ClassFormatter:
    @staticmethod
    def format(path, base_path):
        module_path = path.replace(base_path, '')

        base_name = os.path.basename(base_path)

        module_path = "{}{}".format(base_name, module_path)
        path, extension = os.path.splitext(module_path)

        module_name = os.path.basename(path)
        module_path = path.replace(os.sep, '.')

        return module_path, module_name


class PatternMapper:
    @staticmethod
    def path(path, base_path=None):
        module_path = path.replace(base_path, '')
        module_path, extension = os.path.splitext(module_path)
        module_path = module_path.replace(os.sep, '.')

        path, filename = os.path.split(path)
        attribute, extension = os.path.splitext(filename)
        return "{}.{}".format(module_path, attribute)


class ClassLoader:
    @staticmethod
    def inherits(pattern):
        results = list()
        cls = ClassLoader.find(pattern)
        attribute = cls.__bases__[0].__name__
        module = cls.__bases__[0].__module__
        parent_pattern = ClassLoader._join(module, attribute)

        results.append(parent_pattern)
        if attribute != 'object':
            results.extend(ClassLoader.inherits(parent_pattern))

        return results

    @staticmethod
    def _join(module, attribute):
        return "{}.{}".format(module, attribute)

    @staticmethod
    def _split(pattern):
        nodes = pattern.split('.')
        count = len(nodes)

        module = ".".join(nodes[0:count - 1])
        attribute = nodes[count - 1]
        return module, attribute

    @staticmethod
    def find(pattern):
        invalidate_caches()
        module, attribute = ClassLoader._split(pattern)

        mod = import_module(module)
        cls = getattr(mod, attribute)
        return cls

    @staticmethod
    def load(pattern):
        cls = ClassLoader.find(pattern)
        return cls()



properties = dict()
properties['harc.dir'] = os.path.dirname(harc.__file__)
properties['plugin.dir'] = os.path.join(properties.get('harc.dir'), 'plugins')


harc_dir = properties.get('harc.dir')

print('-------------')
plugin_dir = properties.get('plugin.dir')
folders = Dirs.list(plugin_dir, '__pycache__', True)
for folder in folders:
    files = Files.list(folder, '__init__.py', '^.*\.(py)$')
    for file in files:
        print(file)
        # base_dir = str(Path(harc_dir).parent)
        # pattern = PatternMapper.path(file, base_dir)
        # print(pattern)



exit(0)
