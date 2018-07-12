from datetime import datetime
from datetime import timedelta
from harc.connectors.Helper import Helper
from harc.repositories.Repository import Repository


class LogRepository(Repository):
    def __init__(self, datasource):
        Repository.__init__(self, datasource)

    def list_by_job_name(self, job_name):
        connection = self.get_connection()
        cursor = connection.cursor()
        statement = "select * from log where job_name=:job_name"

        m = {}
        m['job_name'] = job_name

        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)

        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return None
        return result

    def insert(self, message):
        connection = self.get_connection()
        cursor = connection.cursor()
        statement = Helper.statement("insert into log(logtype_code, job_name, package_name, method_name, message, format_error_backtrace) values ({},{},{},{},{},{})", message['logtype_code'], message['job_name'], message['package_name'], message['method_name'], message['message'], message['backtrace'])
        cursor.execute(statement)
        message['id'] = cursor.lastrowid
        connection.commit()
        return message

    def clean(self, days):
        connection = self.get_connection()
        cursor = connection.cursor()

        statement = "delete from log where created_at <:created_at"

        now = datetime.now()
        window = now - timedelta(days=int(days))
        created_at = window.strftime('%Y-%m-%d %H:%M:%S')

        m = {}
        m['created_at'] = created_at

        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)
        count = cursor.rowcount
        cursor.close()
        connection.commit()
        return count
