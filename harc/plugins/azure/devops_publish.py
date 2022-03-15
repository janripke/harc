import logging
import click
from harc.system import git, pypi
from harc.system.release import release_number
from harc.system.release import release_file


class DevopsPublish:
    @click.command()
    @click.option('--feed-name', required=True)
    @click.option('--organization-name', required=True)
    @click.option('--project-name', required=True)
    @click.option('--config-file', required=True)
    @click.option('--branch', required=False)
    @click.pass_context
    def execute(ctx, feed_name, organization_name, project_name, config_file, branch):
        logging.info(f"feed-name: {feed_name}, organization-name: {organization_name}, "
                     f"branch : {branch}, "
                     f"project-name: {project_name}, config-file: {config_file}")

        # retrieve the properties, set by the cli
        properties = ctx.obj

        # if no branch is given, main is assumed.
        if not branch:
            branch = "main"
            logging.info(f"using branch : {branch}")

        tmp_folder = ""

        release = release_file.get_version(tmp_folder, properties['name'], properties['technology'])
        release, snapshot = release.split('-')
        logging.info(f"release={release}, snapshot={str(snapshot)}")
        if not snapshot:

            # checkout the branch
            git.checkout_branch(branch, tmp_folder)

            # build the distribution archives
            logging.info(f"build wheel")
            pypi.build_wheel(tmp_folder)

            # publish the distribution as an azure artifact
            logging.info(f"publish artifact")
            pypi.upload_artifact(feed_name, organization_name, project_name, config_file)

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