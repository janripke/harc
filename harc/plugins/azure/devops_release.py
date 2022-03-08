import logging
import base64
import uuid

from urllib.parse import urlparse, quote
import click

from harc.system.exceptions import PluginException
from harc.system import git
from harc.system import utils
from harc.system.release import release_number
from harc.system.release import release_file
from harc.plugins.git_username_option import GitUsernameOption
from harc.plugins.git_password_option import GitPasswordOption
from harc.system import azure


class DevopsRelease:
    @click.command()
    @click.option('--resource-name', required=False)
    @click.option('--subscription-name', required=False)
    @click.option('--branch', required=False)
    @click.option('--version', required=False)
    @click.pass_context
    def execute(ctx, resource_name, subscription_name, branch, version):
        logging.info(f"resource: {resource_name}, subscription: {subscription_name}"
                     f"branch :{branch}, version: {version}")

        # retrieve the properties, set by the cli
        properties = ctx.obj

        # if no branch is given, master is assumed.
        if not branch:
            branch = "main"
            logging.info("using branch : {}".format(branch))

        result = azure.account_get_access_token(resource_name)
        logging.info(f"{result}")

        token = result['accessToken'].encode('ascii')
        encoded = base64.b64encode(token)
        logging.info(encoded)

        # parse the url, when the scheme is http or https a username, password combination is expected.
        url = urlparse(properties['repository'])
        repository = properties['repository']
        logging.info(f"{repository}")

        if url.scheme in ['http', 'https']:
            repository = f"{url.scheme}://devops:{token}@{url.netloc}{url.path}"

        # set identifier, reflecting the checkout folder to build this release.
        name = uuid.uuid4().hex

        # create an empty folder in tmp
        tmp_folder = utils.recreate_tmp(name)

        # clone the repository to the tmp_folder
        logging.info("clone into {}".format(tmp_folder))
        git.clone(repository, tmp_folder)