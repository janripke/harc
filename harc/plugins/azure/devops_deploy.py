import logging
import click
from harc.system import pypi, databricks, utils
from harc.system.release import release_file


class DevopsDeploy:
    @click.command()
    @click.option('--feed-name', required=True)
    @click.option('--organization-name', required=True)
    @click.option('--project-name', required=True)
    @click.option('--package-name', required=True)
    @click.option('--cluster-name', required=True)
    @click.option('--dbfs-package-path', required=True)
    @click.pass_context
    def execute(ctx, feed_name, organization_name, project_name, package_name: str, cluster_name: str, dbfs_package_path: str):
        logging.info(f"feed-name: {feed_name}, organization-name: {organization_name}, project-name: {project_name}, package-name: {package_name}")

        # retrieve the properties, set by the cli
        properties = ctx.obj

        # this value is given by the release pipeline, when no version is given.
        tmp_folder = ""

        release = release_file.get_version(tmp_folder, properties['name'], properties['technology'])
        logging.info(f"release: {release}")

        # download the package from azure artifacts
        result = pypi.download(feed_name, organization_name, project_name, package_name, release)
        logging.info(f"result={result}")

        logging.info(f"creating remote package folder {dbfs_package_path}")
        databricks.fs_mkdirs(dbfs_package_path)

        wheel = utils.files(f"{properties['name']}*.whl")[0]

        logging.info(f"uploading {wheel} to {dbfs_package_path}")
        databricks.fs_copy(wheel, dbfs_package_path)

        cluster = databricks.cluster_by_name(cluster_name)
        cluster_id = cluster['cluster_id']
        logging.info(f"cluster-id: {cluster_id}")

        if cluster['state'] not in ["RUNNING"]:
            logging.info(f"starting cluster...")
            databricks.cluster_start(cluster_id)

            databricks.cluster_wait_for_start(cluster_id)

        remote_package_path = f"{dbfs_package_path}/{wheel}"
        logging.info(f"installing library {remote_package_path}")
        databricks.libraries_install(cluster_id, remote_package_path)
