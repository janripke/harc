import logging
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
    @click.option('--organization-name', required=True)
    @click.option('--project-name', required=True)
    @click.option('--branch', required=False)
    @click.option('--version', required=False)
    @click.pass_context
    def execute(ctx, organization_name, project_name, branch, version):
        logging.info(f"organization: {organization_name}, "
                     f"project: {project_name}, branch :{branch}, version: {version}")

        # retrieve the properties, set by the cli
        properties = ctx.obj

        # if no branch is given, master is assumed.
        if not branch:
            branch = "main"
            logging.info("using branch : {}".format(branch))

        azure.devops_project_show(organization_name, project_name)
