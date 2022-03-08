from harc.shell import command


def build(folder=None):
    if folder:
        output = command.execute(f"cd {folder};python3 -m build", print_output=True)
    else:
        output = command.execute(f"python3 -m build", print_output=True)
    return command.stringify(output)


def upload(folder, username, password):
    output = command.execute(f"cd {folder};twine upload --username {username} --password '{password}' dist/*")
    return command.stringify(output)