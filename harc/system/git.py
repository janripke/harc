from harc.shell import command


def clone(repository, folder):
    output = command.execute(f"git clone {repository} {folder}")
    return command.stringify(output)


def checkout(version, folder):
    output = command.execute(f"cd {folder};git checkout {version}")
    return command.stringify(output)


def commit(version, folder):
    output = command.execute(f"cd {folder};git commit -a --message='updated to version {version}")
    return command.stringify(output)


def tag(version, folder):
    output = command.execute(f"cd {folder}; git tag -a {version} -m '{version}'")
    return command.stringify(output)


def push(repository, branch, folder):
    output = command.execute(f"cd {folder};git push --tags {repository} {branch}")
    return command.stringify(output)






