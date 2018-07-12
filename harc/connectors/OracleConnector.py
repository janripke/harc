import cx_Oracle


class OracleConnector:

    def __init__(self, datasource):
        self.__username = datasource['username']
        self.__password = datasource['password']
        self.__sid = datasource['sid']
        self.__connection = self.connect()

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_sid(self):
        return self.__sid

    def get_connection(self):
        return self.__connection

    def is_connected(self):
        connection = self.get_connection()
        if connection:
            return True
        return False

    def statement(self, statement, message):
        return statement, message

    def connect(self):
        username = self.get_username()
        password = self.get_password()
        sid = self.get_sid()
        return cx_Oracle.connect(username + '/' + password + '@' + sid)

    def close(self):
        if self.is_connected():
            connection = self.get_connection()
            connection.close()
