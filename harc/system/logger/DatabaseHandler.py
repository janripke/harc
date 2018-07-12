from harc.connectors.DatasourceBuilder import DatasourceBuilder
from harc.repositories.LogRepository import LogRepository


class DatabaseHandler:
    def __init__(self, datasource):
        self.__datasource = datasource

    def get_datasource(self):
        return self.__datasource

    def write(self, message):
        datasource = self.get_datasource()
        log_ds = DatasourceBuilder.find(datasource)
        logger = LogRepository(log_ds)
        logger.insert(message)
        logger.close()
