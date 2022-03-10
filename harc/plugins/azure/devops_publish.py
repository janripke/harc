import logging
import click
from harc.system import git, pypi
from harc.system.release import release_number
from harc.system.release import release_file


class DevopsPublish:
    @click.command()
    @click.option('--feed-name', required=True)
    @click.option('--config-file', required=True)
    @click.pass_context
    def execute(ctx, feed_name, config_file):
        logging.info(f"feed-name: {feed_name}, config-file: {config_file}")

        # retrieve the properties, set by the cli
        properties = ctx.obj

        tmp_folder = ""
        # # build the distribution archives
        logging.info(f"build wheel")
        pypi.build_wheel(tmp_folder)

        # publish the distribution as an azure artifact
        logging.info(f"publish artifact")
        pypi.upload_artifact(feed_name, config_file)
