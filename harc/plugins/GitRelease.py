from harc.plugins.Plugable import Plugable
from harc.plugins.PluginException import PluginException
from harc.system.Git import Git
from harc.system.System import System
from harc.system.release.ReleaseNumber import ReleaseNumber
from harc.system.release.ReleaseFile import ReleaseFile
from urlparse import urlparse
import urllib
import uuid


class GitRelease(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def execute(arguments, settings, properties):

        username = arguments.u
        password = arguments.p
        branch = arguments.b
        v = arguments.v

        projects = settings['projects']

        # if no branche is given, master is assumed.
        if not branch:
            branch = "master"
            print "using branch : " + branch

        for project in projects:

            # parse the url, when the scheme is http or https a username, password combination is expected.
            url = urlparse(project['repository'])
            repository = project['repository']

            if url.scheme in ['http', 'https']:
                if not username:
                    raise PluginException("no username")

                if not password:
                    raise PluginException("no password")

                repository = project['repository'].format(urllib.quote(username), urllib.quote(password))

            # set identifier, reflecting the checkout folder to build this release.
            name = uuid.uuid4().hex

            # create an empty folder in tmp
            tmp_folder = System.create_tmp(name)

            # clone the repository to the tmp_folder
            result = Git.clone(repository, tmp_folder)
            print "clone: " + str(result)

            # list the branches
            branches = Git.branches(tmp_folder)
            if branch not in branches:
                raise PluginException("the given branch " + branch + " is not found.")

            # checkout the branche and switch to it.
            if branch != 'master':
                result = Git.checkout_branch(branch, tmp_folder)
                print result

            # update the version file(s) to the release version.
            # if a version is given, this version is used.
            # if no version is given, the current version is used and snapshot is removed.
            if v:
                ReleaseFile.set_version(tmp_folder, project['name'], project['technology'], v)
                release = v

            if not v:
                release = ReleaseFile.get_version(tmp_folder, project['name'], project['technology'])
                release = release.replace('-SNAPSHOT', '')
                ReleaseFile.set_version(tmp_folder, project['name'], project['technology'], release)

            # commit the changes
            result = Git.commit(release, tmp_folder)
            print result

            # create the tag
            result = Git.tag(release, tmp_folder)
            print result

            # push the changes.
            result = Git.push(repository, branch, tmp_folder)
            print result

            # update the version file(s) to the new snapshot release
            release = ReleaseNumber.increment_build(release)
            release = release + '-SNAPSHOT'
            ReleaseFile.set_version(tmp_folder, project['name'], project['technology'], release)

            # commit the changes
            result = Git.commit(release, tmp_folder)
            print result

            # push the changes.
            result = Git.push(repository, branch, tmp_folder)
            print result


# todo; create a branch