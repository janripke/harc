from subprocess import Popen, PIPE
from harc.shell import command
from harc.system.exceptions import PluginException


def clone(repository, folder):
    statement = "git clone {} {}".format(repository, folder)
    output = command.execute(statement)
    return command.stringify(output)


def branches(folder):
    # statement = "cd " + folder + ";" + "git ls-remote --heads origin"
    statement = "cd {};git ls-remote --heads origin"
    output = command.execute(statement)
    output = command.stringify(output)

    # p = Popen([statement], stdout=PIPE, shell=True)
    # output, error = p.communicate()
    # if p.returncode != 0:
    #     raise PluginException(error)

    output = output.decode('utf-8')
    lines = output.split("\n")
    results = []
    for line in lines:
        if line:
            results.append(line.split("\t")[1].replace('refs/heads/', ''))
    return results


def commit(version, folder):
    statement = "cd {};git commit -a --message='updated to version {}'".format(folder, version)
    output = command.execute(statement)
    return command.stringify(output)


def tag(version, folder):
    # statement = "cd " + folder + ";" + "git tag -a " + version + " -m '" + version + "'"

    statement = "cd {}; git tag -a {} -m '{}'".format(folder, version, version)
    output = command.execute(statement)
    return command.stringify(output)

    # p = Popen([statement], stdout=PIPE, shell=True)
    # output, error = p.communicate()
    # if p.returncode != 0:
    #     raise PluginException(error)
    # return output


def push(repository, branch, folder):
    # statement = "cd " + folder + ";" + "git push --tags " + repository + " " + branch

    statement = "cd {};git push --tags {} {}".format(folder, repository, branch)
    output = command.execute(statement)
    return command.stringify(output)


    # p = Popen([statement], stdout=PIPE, shell=True)
    # output, error = p.communicate()
    # if p.returncode != 0:
    #     raise PluginException(error)
    # return output
