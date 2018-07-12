import hashlib
from harc.connectors.Helper import Helper
from harc.repositories.Repository import Repository
from harc.repositories.SessionRepository import SessionRepository


class UserRepository(Repository):
    def __init__(self, datasource):
        Repository.__init__(self, datasource)

    def find_by_username(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()

        m = {}
        m['username'] = username

        statement = "select * from users where username=:username"
        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()
        if len(result) == 0:
            return None
        return result[0]

    def login(self, username, password):
        user = self.find_by_username(username)
        md5 = hashlib.md5()
        md5.update(password)
        if user:
            if user['password'] == md5.hexdigest():
                session_repository = SessionRepository(self.get_datasource())
                session = session_repository.create()
                session = session_repository.find_by_id(session['id'])
                return session['hashcode']
        return None

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from users")
        return Helper.cursor_to_json(cursor)

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        m = {}
        m['hashcode'] = hashcode

        statement = "select * from users where hashcode=:hashcode"
        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()
        if len(result) == 0:
            return None
        return result[0]
