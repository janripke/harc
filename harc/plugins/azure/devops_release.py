import logging
import click
from harc.system import git, pypi
from harc.system.release import release_number
from harc.system.release import release_file


class DevopsRelease:
    @click.command()
    @click.option('--username', required=True)
    @click.option('--email', required=True)
    @click.option('--branch', required=False)
    @click.option('--version', required=False)
    @click.pass_context
    def execute(ctx, username, email, branch, version):
        logging.info(f"username: {username}, email: {email}, "
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

        # checkout the branch
        git.checkout_branch(branch, tmp_folder)

        # commit the changes
        result = git.commit(release, tmp_folder)
        logging.info(result)

        # create the tag
        logging.info("creating tag {}".format(release))
        git.tag(release, tmp_folder)

        # push the changes.
        logging.info(f"pushing {branch}")
        git.push_tags(branch, tmp_folder)

        # update the version file(s) to the new snapshot release
        dev_release = release_number.increment_build(release)
        dev_release = dev_release + '-dev0'
        release_file.set_version(tmp_folder, properties['name'], properties['technology'], dev_release)

        # commit the changes
        result = git.commit(dev_release, tmp_folder)
        logging.info(result)

        # push the changes.
        logging.info("pushing {}".format(branch))
        git.push_tags(branch, tmp_folder)

        # publish the release
        # checkout the given version
        git.checkout(release, tmp_folder)

        # build the distribution archives
        pypi.build_wheel(tmp_folder)
