import logging
import uuid

from urllib.parse import urlparse, quote
import click

from harc.system.exceptions import PluginException
from harc.system import git, pypi
from harc.system import utils
from harc.system.release import release_number
from harc.system.release import release_file
from harc.plugins.git_username_option import GitUsernameOption
from harc.plugins.git_password_option import GitPasswordOption
from harc.plugins.pypi_username_option import PyPiUsernameOption
from harc.plugins.pypi_password_option import PyPiPasswordOption

class PyPiDeploy:
    @click.command()
    @click.option('-u', '--username', cls=GitUsernameOption, required=True)
    @click.option('-p', '--password', cls=GitPasswordOption, required=True)
    @click.option('-u', '--pypi-username', cls=PyPiUsernameOption, required=True)
    @click.option('-u', '--pypi-password', cls=PyPiPasswordOption, required=True)
    @click.option('-v', '--version', required=True)
    @click.pass_context
    def execute(ctx, username, password, pypi_username, pypi_password, version):
        logging.info(f"{username=}, {version=}")
        # retrieve the properties, set by the cli
        properties = ctx.obj

        # parse the url, when the scheme is http or https a username, password combination is expected.
        url = urlparse(properties['repository'])
        repository = properties['repository']

        if url.scheme in ['http', 'https']:
            repository = f"{url.scheme}://'{quote(username)}':'{quote(password)}'@{url.netloc}{url.path}"

        # set identifier, reflecting the checkout folder to build this release.
        name = uuid.uuid4().hex

        # create an empty folder in tmp
        tmp_folder = utils.recreate_tmp(name)

        # clone the repository to the tmp_folder
        logging.info(f"clone into {tmp_folder}")
        git.clone(repository, tmp_folder)

        # checkout the given version
        git.checkout(version, tmp_folder)

        # build the distribution archives
        pypi.build(tmp_folder)

        # upload the distribution archives to pypi
        pypi.upload(tmp_folder, pypi_username, pypi_password)
        # upload the distribution to https://pypi.org/