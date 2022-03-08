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
    @click.option('--username', required=False)
    @click.option('--email', required=False)
    @click.option('--branch', required=False)
    @click.option('--version', required=False)
    @click.pass_context
    def execute(ctx, resource_name, subscription_name, username, email, branch, version):
        logging.info(f"resource: {resource_name}, subscription: {subscription_name}, "
                     f"username: {username}, email: {email}, "
                     f"branch :{branch}, version: {version}")

        # retrieve the properties, set by the cli
        properties = ctx.obj

        # if no branch is given, main is assumed.
        if not branch:
            branch = "main"
            logging.info(f"using branch : {branch}")

        tmp_folder = ""
        # update the version file(s) to the release version.
        # if a version is given, this version is used.
        # if no version is given, the current version is used and the dev part is removed.
        # the version format 1.0.2-dev0 is expected
        if version:
            release_file.set_version(tmp_folder, properties['name'], properties['technology'], version)
            release = version

        if not version:
            release = release_file.get_version(tmp_folder, properties['name'], properties['technology'])
            release = release.split('-')[0]
            release_file.set_version(tmp_folder, properties['name'], properties['technology'], release)

        git.config_global("user.name", username)
        git.config_global("user.email", email)

        # commit the changes
        result = git.commit(release, tmp_folder)
        logging.info(result)

        # create the tag
        logging.info("creating tag {}".format(release))
        git.tag(release, tmp_folder)

        # push the changes.
        logging.info(f"pushing {branch}")
        git.push_tags(branch, tmp_folder)
