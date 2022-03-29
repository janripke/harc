import logging
from harc.shell import command


def build(folder=None):
    if folder:
        output = command.execute(f"cd {folder};python3 -m build", print_output=True)
    else:
        output = command.execute(f"python3 -m build", print_output=True)
    return command.stringify(output)


def build_wheel(folder=None):
    if folder:
        output = command.execute(f"cd {folder};python setup.py sdist bdist_wheel", print_output=True)
    else:
        output = command.execute(f"python setup.py sdist bdist_wheel", print_output=True)
    return command.stringify(output)


def upload(folder, username, password):
    output = command.execute(f"cd {folder};twine upload --username {username} --password '{password}' dist/*")
    return command.stringify(output)


def upload_artifact(feed_name: str, organization_name: str, project_name: str, config_file: str):
    "twine upload --repository-url https://pkgs.dev.azure.com/<your-organization-name>/<your-project-name>/_packaging/<your-feed-name>/pypi/upload"
    url = f"https://pkgs.dev.azure.com/{organization_name}/{project_name}/_packaging/{feed_name}/pypi/upload"

    output = command.execute(f"twine upload -r '{feed_name}' --config-file {config_file} dist/*.whl", print_output=True)
    return command.stringify(output)


def download(package_name: str, release: str) -> str:
    # index_url = f"https://pkgs.dev.azure.com/{organization_name}/{project_name}/_packaging/{feed_name}/pypi/simple/"

    statement = f"pip download {package_name}=={release} --no-deps"
    output = command.execute(statement, print_output=True)
    return command.stringify(output)
