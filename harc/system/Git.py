from subprocess import Popen, PIPE
from harc.plugins.PluginException import PluginException


class Git(object):
    def __init(self):
        object.__init__(self)

    @staticmethod
    def clone(repository, folder):
        print repository, folder
        statement = "git clone " + repository + " " + folder
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output

    @staticmethod
    def branches(folder):
        statement = "cd " + folder + ";" + "git ls-remote --heads origin"
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)

        lines = output.split("\n")
        results = []
        for line in lines:
            if line:
                results.append(line.split("\t")[1].replace('refs/heads/', ''))
        return results

    @staticmethod
    def checkout_branch(branch, folder):
        statement = "cd " + folder + ";" + "git checkout -b " + branch + " origin/" + branch
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output

        # execSync("git checkout -b " + settings.branch + " origin/" + settings.branch,
        #         {cwd: tmpDirName + "/quad-rest-services"});

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
    def checkout_tag(folder, version):
        statement = "cd " + folder + ";" + "git checkout " + version
        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise PluginException(error)
        return output

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

        results = []
        lines = output.split("\n")
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
