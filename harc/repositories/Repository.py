from harc.connectors.ConnectorFactory import ConnectorFactory


class Repository:
    def __init__(self, datasource):
        self.__datasource = datasource
        connector = ConnectorFactory.create_connector(datasource)
        self.__connector = connector

    def get_datasource(self):
        return self.__datasource

    def get_connector(self):
        return self.__connector

    def get_connection(self):
        connector = self.get_connector()
        return connector.get_connection()

    def statement(self, statement, message):
        connector = self.get_connector()
        return connector.statement(statement, message)

    def has_lastrowid(self):
        datasource = self.get_datasource()
        if datasource['type'] == 'oracle':
            return False
        return True

    def close(self):
        connector = self.get_connector()
        connector.close()