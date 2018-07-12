from harc.repositories.Repository import Repository
from harc.connectors.Helper import Helper


class SessionRepository(Repository):
    def __init__(self, datasource):
        Repository.__init__(self, datasource)

    def create(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        statement = "insert into sessions () values ()"
        cursor.execute(statement)
        session = {}
        session['id'] = cursor.lastrowid
        connection.commit()
        return session;

    def find_by_id(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        m = {}
        m['id'] = id

        statement = "select * from sessions where id=:id"
        statement, parameters = self.statement(statement, m)
        print statement, parameters
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()
        if len(result) == 0:
            return None
        return result[0]

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        m = {}
        m['hashcode'] = hashcode

        statement = "select * from sessions where hashcode=:hashcode and active=1"
        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()
        if len(result) == 0:
            return None
        return result[0]

    def valid(self, hashcode):
        # todo: add valid time in hours, and toggle active to 0 when not valid any more.
        session = self.find_by_hashcode(hashcode)
        if session:
            return True
        return False
