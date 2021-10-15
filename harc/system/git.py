from harc.shell import command


def clone(repository, folder):
    output = command.execute(f"git clone {repository} {folder}")
    return command.stringify(output)


def checkout(version, folder):
    output = command.execute(f"cd {folder};git checkout {version}")
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


def commit(version, folder):
    output = command.execute(f"cd {folder};git commit -a --message='updated to version {version}'")
    return command.stringify(output)


def tag(version, folder):
    output = command.execute(f"cd {folder}; git tag -a {version} -m '{version}'")
    return command.stringify(output)


def push(repository, branch, folder):
    output = command.execute(f"cd {folder};git push --tags {repository} {branch}")
    return command.stringify(output)






