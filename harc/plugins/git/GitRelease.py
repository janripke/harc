from harc.plugins.Plugin import Plugin
from harc.plugins.PluginException import PluginException
from harc.system.Git import Git
from harc.system.System import System
from harc.system.release.ReleaseNumber import ReleaseNumber
from harc.system.release.ReleaseFile import ReleaseFile
from harc.system.Profile import Profile
from harc.plugins.UsernameOption import UsernameOption
from harc.plugins.PasswordOption import PasswordOption
from urllib.parse import urlparse, quote
import uuid
import logging
import click


class GitRelease:
    @click.command()
    @click.option('-u', '--username', cls=UsernameOption, required=True)
    @click.option('-p', '--password', cls=PasswordOption, required=True)
    @click.option('-b', '--branch', required=False)
    @click.option('-v', '--version', required=False)
    @click.pass_context
    def execute(ctx, username, password, branch, version):
        logger = logging.getLogger()
        logger.info("username :{}, branche :{}, version: {}".format(username, branch, version))

        # retrieve the properties, set by the cli
        properties = ctx.obj

        # username = arguments.u
        # password = arguments.p
        # branch = arguments.b
        # v = arguments.v

        # if no branche is given, master is assumed.
        if not branch:
            branch = "master"
            print("using branch : " + branch)

        # parse the url, when the scheme is http or https a username, password combination is expected.
        url = urlparse(properties['repository'])
        repository = properties['repository']

        if url.scheme in ['http', 'https']:
            repository = url.scheme + "://'{0}':'{1}'@" + url.netloc + url.path
            repository = repository.format(quote(username), quote(password))

        # set identifier, reflecting the checkout folder to build this release.
        name = uuid.uuid4().hex

        # create an empty folder in tmp
        tmp_folder = System.recreate_tmp(name)

        # clone the repository to the tmp_folder
        print("Clone:")
        result = Git.clone(repository, tmp_folder)
        print(str(result))

        # list the branches
        branches = Git.branches(tmp_folder)
        if branch not in branches:
            raise PluginException("the given branch {} is not found.".format(branch))

        # checkout the branche and switch to it.
        if branch != 'master':
            result = Git.checkout_branch(branch, tmp_folder)
            print(result)

        # update the version file(s) to the release version.
        # if a version is given, this version is used.
        # if no version is given, the current version is used and snapshot is removed.
        if version:
            ReleaseFile.set_version(tmp_folder, properties['name'], properties['technology'], version)
            release = version

        if not version:
            release = ReleaseFile.get_version(tmp_folder, properties['name'], properties['technology'])
            release = release.replace('-SNAPSHOT', '')
            ReleaseFile.set_version(tmp_folder, properties['name'], properties['technology'], release)

        # commit the changes
        result = Git.commit(release, tmp_folder)
        print(result)

        # create the tag
        result = Git.tag(release, tmp_folder)
        print(result)

        # push the changes.
        result = Git.push(repository, branch, tmp_folder)
        print(result)

        # update the version file(s) to the new snapshot release
        release = ReleaseNumber.increment_build(release)
        release = release + '-SNAPSHOT'
        ReleaseFile.set_version(tmp_folder, properties['name'], properties['technology'], release)

        # commit the changes
        result = Git.commit(release, tmp_folder)
        print(result)

        # push the changes.
        result = Git.push(repository, branch, tmp_folder)
        print(result)


# todo; create a branch