import logging
from harc.shell import command


def clone(repository, folder):
    output = command.execute(f"git clone {repository} {folder}")
    return command.stringify(output)


def checkout(version, folder=None):
    if folder:
        output = command.execute(f"cd {folder};git checkout {version}")
    else:
        output = command.execute(f"git checkout {version}")
    return command.stringify(output)


def checkout_branch(branch: str, folder=None):
    if folder:
        output = command.execute(f"cd {folder};git checkout -b {branch}")
    else:
        output = command.execute(f"git checkout -b {branch}")
    return command.stringify(output)


def branches(folder):
    # statement = "cd " + folder + ";" + "git ls-remote --heads origin"
    statement = f"cd {folder};git ls-remote --heads origin"
    output = command.execute(statement)
    output = command.stringify(output)

    # p = Popen([statement], stdout=PIPE, shell=True)
    # output, error = p.communicate()
    # if p.returncode != 0:
    #     raise PluginException(error)

    lines = output.split("\n")
    results = []
    for line in lines:
        if line:
            results.append(line.split("\t")[1].replace('refs/heads/', ''))
    return results


def commit(version, folder=None):
    if folder:
        output = command.execute(f"cd {folder};git commit -a --message='updated to version {version}'")
    else:
        output = ""
        logging.info(f"git commit -a --message='updated to version {version}'")
        # output = command.execute(f"git commit -a --message='updated to version {version}'")
    return command.stringify(output)


def tag(version, folder=None):
    if folder:
        output = command.execute(f"cd {folder}; git tag -a {version} -m '{version}'")
    else:
        output = command.execute(f"git tag -a '{version}' -m '{version}'")
    return command.stringify(output)


def push(repository, branch, folder):
    output = command.execute(f"cd {folder};git push --tags {repository} {branch}")
    return command.stringify(output)


def push_tags(branch: str, folder=None):
    if folder:
        output = command.execute(f"cd {folder};git push --tags origin {branch}")
    else:
        # output = command.execute(f"git push -u origin {branch} --tags")
        output = command.execute(f"git push --tags -u origin {branch}")
    return command.stringify(output)


def config_global(key: str, value: str):
    output = command.execute(f"git config --global {key} {value}")
    return command.stringify(output)




