import logging
import time
from harc.shell import command
from harc.system import exceptions


def clusters_list():

    output = command.execute(f"databricks clusters list --output JSON")
    return command.dictify(output)


def cluster_by_name(cluster_name: str):
    clusters = clusters_list()
    for cluster in clusters.get('clusters'):
        if cluster['cluster_name'] == cluster_name:
            return cluster


def cluster_by_id(cluster_id: str):
    clusters = clusters_list()
    for cluster in clusters.get('clusters'):
        if cluster['cluster_id'] == cluster_id:
            return cluster


def cluster_start(cluster_id: str):
    output = command.execute(f"databricks clusters start --cluster-id {cluster_id}")
    return command.dictify(output)


def cluster_wait_for_start(cluster_id: str, interval: int = 10, timeout: int = 60):
    state = ""
    count = 0
    while state not in ['RUNNING']:
        cluster = cluster_by_id(cluster_id)
        state = cluster["state"]

        logging.info(f"state={state}")

        if count >= timeout:
            raise exceptions.DatabricksError(f"timeout")

        count += 1
        time.sleep(interval)


def fs_mkdirs(remote_path: str):
    output = command.execute(f"databricks fs mkdirs '{remote_path}'")
    return command.stringify(output)


def fs_copy(path: str, remote_path: str):
    output = command.execute(f"databricks fs cp --overwrite {path} '{remote_path}'")
    return command.stringify(output)


def databricks_libraries_list(cluster_id: str):
    output = command.execute(f"databricks libraries list")
    output = command.dictify(output)
    statuses = output.get("statuses")
    for status in statuses:
        if status["cluster_id"] == cluster_id:
            return status


def libraries_install(cluster_id: str, remote_path: str):
    output = command.execute(f"databricks libraries install --cluster-id {cluster_id} --whl {remote_path}")
    return command.stringify(output)


def libraries_uninstall(cluster_id: str, remote_path: str):
    output = command.execute(f"databricks libraries uninstall --cluster-id {cluster_id} --whl {remote_path}")
    return command.stringify(output)