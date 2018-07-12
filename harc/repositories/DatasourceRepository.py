from harc.repositories.Repository import Repository
from harc.connectors.Helper import Helper


class DatasourceRepository(Repository):
    def __init__(self, datasource):
        Repository.__init__(self, datasource)

    def get_by_name(self, name):
        connection = self.get_connection()
        cursor = connection.cursor()
        statement = Helper.statement("select * from datasources where name={}", name)
        cursor.execute(statement)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return None
        return result[0]

