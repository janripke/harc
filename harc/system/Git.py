import os
from subprocess import Popen, PIPE
from urllib.parse import urlparse

from harc.shell.Command import Command
from harc.plugins.PluginException import PluginException


class Git(object):
    @staticmethod
    def clone(repository, folder):

        statement = "git clone {} {}".format(repository, folder)
        output = Command.execute(statement)
        return Command.stringify(output)

    @staticmethod
    def branches(folder):
        statement = "cd " + folder + ";" + "git ls-remote --heads origin"
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)

        output = output.decode('utf-8')
        lines = output.split("\n")
        results = []
        for line in lines:
            if line:
                results.append(line.split("\t")[1].replace('refs/heads/', ''))
        return results

    # Instead of checkout_branch and checkout_tag, I am using one method checkout() to avoid confusion since
    # both tag and branch refer to refs in git and checkout works for both. version refers to both tag and branch

    @staticmethod
    def checkout(version, folder):
        statement = "cd {};git checkout {};".format(folder, version)
        output = Command.execute(statement)
        return Command.stringify(output)


    @staticmethod
    def commit(version, folder):
        statement = "cd " + folder + ";" + "git commit -a --message='updated to version " + version + "'"
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output
        # git commit --message='Updated version to " + version +  "'", {cwd: tmpDirName + "/quad-helpdesk"})


    @staticmethod
    def tag(version, folder):
        statement = "cd " + folder + ";" + "git tag -a " + version + " -m '" + version + "'"
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output
        #execSync("git tag -a " + tag + " -m 'quad-helpdesk tag " + tag + "'", {cwd: tmpDirName + "/quad-helpdesk"});

    @staticmethod
    def tags(folder):
        statement = "cd " + folder + ";" + "git tag"
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)

        output = output.decode('utf-8')
        lines = output.split("\n")
        results = []
        for line in lines:
            if line:
                results.append(line)
        return results

    @staticmethod
    def push(repository, branch, folder):
        statement = "cd " + folder + ";" + "git push --tags " + repository + " " + branch
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output
        # execSync("git push --tags " + gitUrlWithCredentials(repos.helpdesk) + " " + settings.branch, {cwd: tmpDirName + "/quad-helpdesk"});

    @staticmethod
    def get_credentials():
        """
        Look in the current user's homedir for a .git-credentials file and parse the paths for use
        by for example docker's requirements file generation functionality.

        :return: A dict like so: {'example.com': {'user': 'bar', 'password': 'baz'}}
        """
        credentials_file = os.path.expanduser('~/.git-credentials')
        results = {}
        if os.path.isfile(credentials_file):
            with open(credentials_file) as f:
                for line in f:
                    if line.strip():
                        url = urlparse(line)
                        if url.hostname and url.username and url.password:
                            results[url.hostname.strip()] = {
                                'user': url.username, 'password': url.password
                            }

        return results
