from importlib import util, import_module, invalidate_caches
from pathlib import Path
import os.path
import harc
import re

properties = dict()
properties['harc.dir'] = os.path.dirname(harc.__file__)
properties['plugin.dir'] = os.path.join(properties.get('harc.dir'), 'plugins')


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
    def list(path, excludes=[], recursive=False, depth=-1):
        results = list()
        elements = os.listdir(path)
        for element in elements:
            node = os.path.join(path, element)
            if os.path.isdir(node) and element not in excludes:
                results.append(node)
            if recursive and os.path.isdir(node):
                if depth > 1 or depth == -1:
                    if depth != -1:
                        depth -= 1
                    results.extend(Dirs.list(node, excludes, recursive, depth))
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


class ModuleLoader:

    @staticmethod
    def load_by_path(name, path):
        spec = util.spec_from_file_location(name, path)
        mod = util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    @staticmethod
    def load_by_name(name, refresh=False):
        if refresh:
            invalidate_caches()

        mod = import_module(name)
        return mod


class ClassLoader:
    @staticmethod
    def load_by_path(name, class_name, path):
        mod = ModuleLoader.load_by_path(name, path)

        if hasattr(mod, class_name):
            cls = getattr(mod, class_name)
            return cls()

    @staticmethod
    def load_by_name(name, class_name, refresh=False):
        mod = ModuleLoader.load_by_name(name, refresh)

        if hasattr(mod, class_name):
            cls = getattr(mod, class_name)
            return cls()

    @staticmethod
    def load_by_pattern(pattern, refresh=False):
        module_name, class_name = ClassPattern(pattern).name()
        mod = ModuleLoader.load_by_name(module_name, refresh)

        if hasattr(mod, class_name):
            cls = getattr(mod, class_name)
            return cls()


class BasePath:
    def __init__(self, path):
        self.__path = path

    def get_path(self):
        return self.__path


class ModulePath(BasePath):
    def name(self, root_dir=None, base_package=None):
        """
        return a qualified module name based on the given root_dir and base_package.

        :param root_dir: the root_dir to get as starting point of the module name.
        :param base_package: the qualified name to add at the beginning of the module name.
        :return: A qualified module name.
        """
        path = self.get_path()

        filepath, filename = os.path.split(path)
        name, ext = os.path.splitext(filename)

        module_name = name

        if root_dir:
            module_name = str(Path(os.path.join(filepath, name)).relative_to(Path(root_dir).parent)).replace(os.sep, '.')

        if base_package:
            module_name = "{}.{}".format(base_package, module_name)

        return module_name


class ClassPath(BasePath):
    def name(self, root_dir=None, base_package=None):
        path = self.get_path()
        module_name = ModulePath(path).name(root_dir, base_package)

        fragments = module_name.rsplit('.', 1)
        class_name = fragments[1]
        return module_name, class_name


class ClassPattern:
    def __init__(self, pattern):
        self.__pattern = pattern

    def get_pattern(self):
        return self.__pattern

    def name(self):
        pattern = self.get_pattern()

        fragments = pattern.rsplit('.', 1)
        module_name = fragments[0]
        class_name = fragments[1]
        return module_name, class_name


plugin_dir = properties.get('plugin.dir')
folders = Dirs.list(plugin_dir, '__pycache__', True, depth=2)
for folder in folders:
    files = Files.list(folder, ['__init__.py'], '^.*\.(py)$')
    for file in files:
        # scenario from file
        # name = ModulePath(file).name(plugin_dir, 'harc.ext')
        # mod = ModuleLoader.load(name, file)
        # print(mod)

        # scenario from module
        # name = ModulePath(file).name(plugin_dir, 'harc')
        module_name, class_name = ClassPath(file).name(plugin_dir, 'harc.ext')
        plugin = ClassLoader.load_by_path(module_name, class_name, file)
        print(plugin)


    #     # a tested classloader, wip
    #     plugin = ClassLoader.load(file, plugin_dir, 'harc.ext')
    #     print("plugin", plugin, file)
    #     # print(name, path, file, Path(file).relative_to(plugin_dir))
    # #
    # #     spec = util.spec_from_file_location(name, file)
    # #     mod = util.module_from_spec(spec)
    # #     spec.loader.exec_module(mod)
    # #     #
    # #     if hasattr(mod, name):
    # #         cls = getattr(mod, name)
    # #         plugin = cls()
    # #         # print(plugin)




        # print(ModuleMapper.path(file, base_path))
exit(0)





# module, package als methode om modules en packages te instantieren
# module, package patroon implementeren, apart
# goeie naam verzinnen voor de scanner, is nu hoofdcode zonder naam.
# load_module, en de module bestaat niet levert een warning op dit gaat niet fout
# kan worden gebruikt in verschillende projecten, apart project (lithium)