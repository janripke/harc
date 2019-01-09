from urllib.parse import urlparse, quote
from harc.plugins.PluginException import PluginException


class PipUrl:
    @staticmethod
    def build(name, version, repository, username, password, no_dependencies=True, no_quote=False, subdirectory=None):
        # retrieve the dependency details
        module_name = name
        module_version = version
        module_repo = repository

        module = module_name

        # if module_version:
        #     if subdirectory:
        #         module = module_name + "@" + module_version + "\&" + subdirectory
        #     else:
        #         module = module_name + "@" + module_version

        if module_repo:
            module_url = urlparse(module_repo)

            if module_url.scheme in ['http', 'https']:
                if not username:
                    raise PluginException("no username")

                if not password:
                    raise PluginException("no password")

                module = "git+" + module_url.scheme + "://{0}:{1}@" + module_url.netloc + module_url.path + " --upgrade"
                if no_dependencies:
                    module = module + " --no-dependencies"
                if no_quote:
                    module = module.format(username, password)
                if not no_quote:
                    module = module.format(quote(username), quote(password))

                if module_version:
                    if subdirectory:
                        module = "git+" + module_url.scheme + "://{0}:{1}@" + module_url.netloc + module_url.path + '@' + module_version + "\&" + subdirectory + " --upgrade"
                    else:
                        module = "git+" + module_url.scheme + "://{0}:{1}@" + module_url.netloc + module_url.path + '@' + module_version + " --upgrade"
                    if no_dependencies:
                        module = module + " --no-dependencies"
                    if no_quote:
                        module = module.format(username, password)
                    if not no_quote:
                        module = module.format(quote(username), quote(password))
        return module
