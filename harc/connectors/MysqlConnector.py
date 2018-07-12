import MySQLdb

from harc.system.Strings import Strings


class MysqlConnector:

    def __init__(self, datasource):
        self.__host = datasource['host']
        self.__username = datasource['username']
        self.__password = datasource['password']
        self.__database = datasource['db']
        self.__connection = self.connect()

    def get_host(self):
        return self.__host

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_database(self):
        return self.__database

    def get_connection(self):
        return self.__connection

    def is_connected(self):
        connection = self.get_connection()
        if connection:
            return True
        return False

    def statement(self, statement, message):
        p = []
        s = statement
        # bindings = statement.split(':')
        # bindings = bindings[1:]
        # print bindings
        # print statement
        # result = []
        # for binding in bindings:
        #     binding = binding.rstrip(' ')
        #     binding = binding.rstrip(',')
        #     binding = binding.rstrip(')')
        #     result.append(binding)

        keywords = Strings.keywords(s, ':')
        for keyword in keywords:
            s = s.replace(':' + keyword, '%s')
            p.append(message[keyword])

        # for r in result:
        #     s = s.replace(':' + r, '%s')
        #     p.append(message[r])

        return s, tuple(p)

    def connect(self):
        host = self.get_host()
        username = self.get_username()
        password = self.get_password()
        database = self.get_database()
        return MySQLdb.connect(host, username, password, database)

    def close(self):
        if self.is_connected():
            connection = self.get_connection()
            connection.close()
