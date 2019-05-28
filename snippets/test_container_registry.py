from harc.azure.AzContainerRegistry import AzContainerRegistry

resource_group_name = "sandbox-nl42949-002-rg"
registries = AzContainerRegistry.list(resource_group=resource_group_name)
for registry in registries:
    print(registry.get('loginServer'))
exit(0)