from urllib.parse import urlparse, quote
from harc.plugins.PluginException import PluginException


class PipUrl:
    @staticmethod
    def build(name, version, repository, username, password, no_dependencies=True):
        # retrieve the dependency details
        module_name = name
        module_version = version
        module_repo = repository

        module = module_name

        if module_version:
            module = module_name + "==" + module_version

        if module_repo:
            module = module_repo
            module_url = urlparse(module_repo)

            if module_url.scheme in ['http', 'https']:
                if not username:
                    raise PluginException("no username")

                if not password:
                    raise PluginException("no password")

                module = "git+" + module_url.scheme + "://'{0}':'{1}'@" + module_url.netloc + module_url.path + " --upgrade"
                if no_dependencies:
                    module = module + " --no-dependencies"
                module = module.format(quote(username), quote(password))

                if module_version:
                    module = "git+" + module_url.scheme + "://'{0}':'{1}'@" + module_url.netloc + module_url.path + '@' + module_version + " --upgrade"
                    if no_dependencies:
                        module = module + " --no-dependencies"
                    module = module.format(quote(username), quote(password))
        return module