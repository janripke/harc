

class Plugin(object):
    _connectable = None

    def __init__(self, connectable=None):
        # self._connector = connectable
        if connectable:
            self._connector = connectable
        else:
            self._connector = self._connectable

    def console(self):
        print("console", self._connector)


class MssqlPlugin(Plugin):
    _connectable = "mssql"


class PostgreSqlPlugin(MssqlPlugin):
    _connectable = "postgres"

    def show(self):
        print("show", self._connector)


class UpdatePlugin(MssqlPlugin):
    def output(self):
        pass


class MysqlPlugin(Plugin):
    _connectable = "mysql"


class Example(object):
    def __init__(self, connectable):
        self._connectable = connectable

    def console(self):
        print("console", self._connectable)


class ExamplePlugin(Example):
    def __init__(self):
        Example.__init__(self, "example")

    def show(self):
        print("show", self._connectable)


class CreatePlugin(ExamplePlugin):
    pass



example = CreatePlugin()
example.console()
example.show()

mssql = MssqlPlugin()
print(mssql._connectable)

mysql = MysqlPlugin()
print(mysql._connectable)
print(mssql._connectable)

postgres = PostgreSqlPlugin()
postgres.show()
postgres.console()




