from harc.connectors.Helper import Helper
from harc.repositories.Repository import Repository
from harc.system.logger.Logger import Logger


class CommandRepository(Repository):
    def __init__(self, datasource):
        Repository.__init__(self, datasource)

    def find_by_name(self, content):
        logger = Logger(self)
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "select * from commands where name=:name and environment=:environment"

        m = {}
        m['name'] = content['command']
        m['environment'] = content['environment']
        statement, parameters = self.statement(statement, m)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return None
        return result[0]



