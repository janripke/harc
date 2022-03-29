import os
import logging
import click
from harc.system import pypi, databricks, utils
from harc.system.release import release_file


class DevopsDeploy:
    @click.command()
    @click.option('--package-name', required=True)
    @click.option('--cluster-name', required=True)
    @click.option('--dbfs-package-path', required=True)
    @click.pass_context
    def execute(ctx, package_name: str, cluster_name: str, dbfs_package_path: str):
        logging.info(f"package-name: {package_name}, cluster-name: {cluster_name}, dbfs-package-path: {dbfs_package_path}")

        # retrieve the properties, set by the cli
        properties = ctx.obj

        # this value is given by the release pipeline, when no version is given.
        tmp_folder = ""

        logging.info(f"DATABRICKS_HOST={os.getenv('DATABRICKS_HOST')}")
        logging.info(f"DATABRICKS_TOKEN={os.getenv('DATABRICKS_TOKEN')}")

        release = release_file.get_version(tmp_folder, properties['name'], properties['technology'])
        logging.info(f"release: {release}")

        # download the package from azure artifacts
        pypi.download(package_name, release)

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

        # uninstall older packages
        libraries = databricks.databricks_libraries_list(cluster_id)
        logging.info(f"{libraries}")
        library_statuses = libraries.get("library_statuses")
        logging.info(f"{library_statuses}")
        for library_status in library_statuses:
            library = library_status.get("library")
            remote_package_path = library.get("whl")
            logging.info(f"library={library}, remote_package_path={remote_package_path}, package_name={package_name}, wheel={wheel}")
            if package_name in remote_package_path and wheel not in remote_package_path:
                logging.info(f"uninstalling library {remote_package_path}")
                databricks.libraries_uninstall(cluster_id, remote_package_path)

        remote_package_path = f"{dbfs_package_path}/{wheel}"
        logging.info(f"installing library {remote_package_path}")
        databricks.libraries_install(cluster_id, remote_package_path)
