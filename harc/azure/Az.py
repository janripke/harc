from subprocess import Popen, PIPE
from greppel.exceptions.CommandException import CommandException
from greppel.system.Command import Command
from greppel.system.Parameter import Parameter


class AzServicePrincipal(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(subscription):
        statement = "az ad sp list {} --all".format(Parameter.format('--subscription', subscription))
        print(statement)
        output = Command.execute(statement)
        return Command.jsonify(output)


class AzVirtualMachine(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(subscription=None, resource_group=None):
        statement = "az vm list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)


class AzKeyVault(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(subscription=None, resource_group=None):
        statement = "az keyvault list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)


class AzContainer(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(subscription=None, resource_group=None):
        statement = "az container list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)


class AzContainerRegistryRepository(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(registry):
        statement = "az acr repository list {}".format(
            Parameter.format('--name', registry)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)


class AzContainerRegistry(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(subscription=None, resource_group=None):
        statement = "az acr list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def find(name, subscription=None, resource_group=None):
        registrations = AzContainerRegistry.list(subscription, resource_group)
        for registration in registrations:
            if registration['name'] == name:
                return registration

    @staticmethod
    def exists(name, subscription=None, resource_group=None):
        if AzContainerRegistry.find(name, subscription, resource_group):
            return True
        return False

    @staticmethod
    def create(name, resource_group, sku, location=None, subscription=None):
        statement = "az acr create {} {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--sku', sku),
            Parameter.format('--location', location),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def delete(name, resource_group, subscription=None):
        statement = "az acr delete {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)


class AzPostgresFirewall(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(server, subscription=None, resource_group=None):
        statement = "az postgres server firewall-rule list {} {} {}".format(
            Parameter.format('--server-name', server),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def find(name, server, subscription=None, resource_group=None):
        rules = AzPostgresFirewall.list(server, subscription, resource_group)
        for rule in rules:
            if rule['name'] == name:
                return rule

    @staticmethod
    def exists(name, server, subscription=None, resource_group=None):
        if AzPostgresFirewall.find(name, server, subscription, resource_group):
            return True
        return False

    @staticmethod
    def create(name, server, start_ip_address, end_ip_address, subscription=None, resource_group=None):
        statement = "az postgres server firewall-rule create {} {} {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--start-ip-address', start_ip_address),
            Parameter.format('--end-ip-address', end_ip_address),
            Parameter.format('--server-name', server),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def delete(name, server, subscription=None, resource_group=None):
        statement = "az postgres server firewall-rule delete --yes {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--server-name', server),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)


class AzPostgresVnet(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(server, subscription=None, resource_group=None):
        statement = "az postgres server vnet-rule list {} {} {}".format(
            Parameter.format('--server-name', server),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)


class AzPostgresDatabase(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(server, resource_group=None, subscription=None):
        statement = "az postgres db list {} {} {}".format(
            Parameter.format('--server-name', server),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def find(name, server, resource_group=None, subscription=None):
        databases = AzPostgresDatabase.list(server, resource_group, subscription)
        for database in databases:
            if database['name'] == name:
                return database

    @staticmethod
    def exists(name, server, resource_group=None, subscription=None):
        if AzPostgresDatabase.find(name, server, resource_group, subscription):
            return True
        return False

    @staticmethod
    def create(name, server, charset=None, resource_group=None, subscription=None):
        statement = "az postgres db create {} {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--server-name', server),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group),
            Parameter.format('--charset', charset)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def delete(name, server ,resource_group=None, subscription=None):
        statement = "az postgres db delete --yes {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--server-name', server),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)


class AzPostgres(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(subscription=None, resource_group=None):
        statement = "az postgres server list {} {}".format(Parameter.format('--subscription', subscription),
                                                           Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def find(name, subscription=None, resource_group=None):
        postgres_servers = AzPostgres.list(subscription, resource_group)
        for postgres_server in postgres_servers:
            if postgres_server['name'] == name:
                return postgres_server

    @staticmethod
    def exists(name, subscription=None, resource_group=None):
        if AzPostgres.find(name, subscription, resource_group):
            return True
        return False

    @staticmethod
    def create(name, resource_group, location, sku, admin_user, admin_password, tags=None):
        statement = "az postgres server create {} {} {} {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--resource-group', resource_group),
            Parameter.format('--location', location),
            Parameter.format('--sku-name', sku),
            Parameter.format('--admin-user', admin_user),
            Parameter.format('--admin-password', admin_password),
            Parameter.format('--tags', tags)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def delete(name, subscription=None, resource_group=None):
        statement = "az postgres server delete {} {} {} --yes".format(
            Parameter.format('--name', name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group)
        )
        output = Command.execute(statement)
        print(output)
        return Command.jsonify(output)


class AzResourceGroup(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(subscription=None):
        statement = "az group list {}".format(Parameter.format('--subscription', subscription))
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def find(name, subscription=None):
        resource_groups = AzResourceGroup.list(subscription)
        print(len(resource_groups))
        for resource_group in resource_groups:
            print(resource_group['name'], name)
            if resource_group['name'] == name:
                return resource_group


class AzIdentity(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(resource_group=None, subscription=None):
        statement = "az identity list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group))
        output = Command.execute(statement)
        return Command.jsonify(output)


class AzStorageContainer(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(account_name, account_key, subscription=None):
        statement = "az storage container list {} {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--account-name', account_name),
            Parameter.format('--account-key', account_key)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def find(name, account_name, account_key, subscription=None):
        containers = AzStorageContainer.list(account_name, account_key, subscription)
        for container in containers:
            if container['name'] == name:
                return container

    @staticmethod
    def exists(name, account_name, account_key, subscription=None):
        statement = "az storage container exists {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--account-name', account_name),
            Parameter.format('--account-key', account_key)
        )
        output = Command.execute(statement)
        output = Command.jsonify(output)

        if output:
            return output.get('exists', False)
        return False

    @staticmethod
    def create(name, account_name, account_key, subscription=None, public_access='off'):
        statement = "az storage container create {} {} {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--account-name', account_name),
            Parameter.format('--account-key', account_key),
            Parameter.format('--public-access', public_access)
        )
        output = Command.execute(statement)
        print(output)
        return Command.jsonify(output)


class AzStorageBlob(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(container_name, account_name, account_key, subscription=None):
        statement = "az storage blob list {} {} {} {}".format(
            Parameter.format('--container-name', container_name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--account-name', account_name),
            Parameter.format('--account-key', account_key)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def upload(container_name, path, name, account_name, account_key, subscription=None, metadata=None):
        statement = "az storage blob upload {} {} {} {} {} {} {}".format(
            Parameter.format('--container-name', container_name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--account-name', account_name),
            Parameter.format('--account-key', account_key),
            Parameter.format('--file', path),
            Parameter.format('--name', name),
            Parameter.format('--metadata', metadata)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)


class AzStorageAccount(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def list(subscription=None, resource_group=None):
        statement = "az storage account list {} {}".format(
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group)
        )
        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def find(subscription, name):
        storage_accounts = AzStorageAccount.list(subscription)
        for storage_account in storage_accounts:
            if storage_account['name'] == name:
                return storage_account

    @staticmethod
    def connection_string(name, subscription=None, resource_group=None):
        statement = "az storage account show-connection-string {} {} {}".format(
            Parameter.format('--name', name),
            Parameter.format('--subscription', subscription),
            Parameter.format('--resource-group', resource_group)
        )

        output = Command.execute(statement)
        return Command.jsonify(output)

    @staticmethod
    def create():
        pass


class Az(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def login(username, password):
        statement = "az login --username {} --password {}".format(username, password)

        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise CommandException(error)
        return output

    @staticmethod
    def storage_accounts(subscription):
        statement = "az storage account list --subscription '{}'".format(subscription)

        p = Popen([statement], stdout=PIPE, shell=True)
        output, error = p.communicate()
        if p.returncode != 0:
            raise CommandException(error)
        return output

