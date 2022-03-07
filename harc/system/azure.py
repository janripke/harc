from harc.shell import command


def devops_project_show(organization_name : str,project_name: str):
    output = command.execute(f"az devops project show "
                             f"--project '{project_name}' "
                             f"--organization https://dev.azure.com/{organization_name}/")
    return command.dictify(output)


def account_get_access_token(subscription_name: str):
    output = command.execute(f"az account get-access-token --subscription {subscription_name}")
    return command.dictify(output)