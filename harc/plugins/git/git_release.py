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


class GitRelease:
    @click.command()
    @click.option('-u', '--username', cls=GitUsernameOption, required=True)
    @click.option('-p', '--password', cls=GitPasswordOption, required=True)
    @click.option('-b', '--branch', required=False)
    @click.option('-v', '--version', required=False)
    @click.pass_context
    def execute(ctx, username, password, branch, version):
        logging.info("username :{}, branch :{}, version: {}".format(username, branch, version))

        # retrieve the properties, set by the cli
        properties = ctx.obj

        # username = arguments.u
        # password = arguments.p
        # branch = arguments.b
        # v = arguments.v

        # if no branch is given, master is assumed.
        if not branch:
            branch = "main"
            logging.info("using branch : {}".format(branch))

        # parse the url, when the scheme is http or https a username, password combination is expected.
        url = urlparse(properties['repository'])
        repository = properties['repository']

        if url.scheme in ['http', 'https']:
            repository = url.scheme + "://'{0}':'{1}'@" + url.netloc + url.path
            repository = repository.format(quote(username), quote(password))

        # set identifier, reflecting the checkout folder to build this release.
        name = uuid.uuid4().hex

        # create an empty folder in tmp
        tmp_folder = utils.recreate_tmp(name)

        # clone the repository to the tmp_folder
        logging.info("clone into {}".format(tmp_folder))
        git.clone(repository, tmp_folder)

        # list the branches
        branches = git.branches(tmp_folder)
        if branch not in branches:
            raise PluginException("the given branch {} is not found.".format(branch))

        # checkout the branch and switch to it.
        # if branch != 'main':
        #     result = git.checkout_branch(branch, tmp_folder)
        #     print(result)

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

        # commit the changes
        result = git.commit(release, tmp_folder)
        logging.info(result)

        # create the tag
        logging.info("creating tag {}".format(release))
        git.tag(release, tmp_folder)

        # push the changes.
        logging.info("pushing {}".format(branch))
        git.push(repository, branch, tmp_folder)

        # update the version file(s) to the new snapshot release
        release = release_number.increment_build(release)
        release = release + '-dev0'
        release_file.set_version(tmp_folder, properties['name'], properties['technology'], release)

        # commit the changes
        result = git.commit(release, tmp_folder)
        logging.info(result)

        # push the changes.
        logging.info("pushing {}".format(branch))
        git.push(repository, branch, tmp_folder)

