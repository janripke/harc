import logging
import click
from harc.system import git
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

        # this value is given by the release pipeline, when no version is given.
        if version and version == "automatically":
            version = None

        # if no branch is given, main is assumed.
        if not branch:
            branch = "main"
            logging.info(f"using branch : {branch}")

        tmp_folder = ""

        git.config_global("user.name", username)
        git.config_global("user.email", email)

        # checkout the branch
        result = git.checkout_branch(branch, tmp_folder)
        logging.info(f"git.checkout_branch={result}")

        # update the version file(s) to the release version.
        # if a version is given, this version is used.
        # if no version is given, the current version is used and the dev part is removed.
        # the version format 1.0.2-dev0 is expected
        if version:
            release_file.set_version(tmp_folder, properties['name'], properties['technology'], version)
            release = version

        if not version:
            release = release_file.get_version(tmp_folder, properties['name'], properties['technology'])
            logging.info(f"release={release}")
            release = release.split('-')[0]
            release_file.set_version(tmp_folder, properties['name'], properties['technology'], release)
            logging.info(f"release={release}")

        # commit the changes
        result = git.commit(release, tmp_folder)
        logging.info(result)

        # create the tag
        logging.info("creating tag {}".format(release))
        git.tag(release, tmp_folder)

        # push the changes.
        logging.info(f"pushing {branch}")
        git.push_tags(branch, tmp_folder)
