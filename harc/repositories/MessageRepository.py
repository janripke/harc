from harc.connectors.Helper import Helper
from harc.repositories.Repository import Repository
from harc.system.Ora import Ora


class MessageException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return repr(self.__message)

    def get_message(self):
        return self.__message


class MessageRepository(Repository):
    def __init__(self, datasource):
        Repository.__init__(self, datasource)

    def insert(self, queue, message):
        # todo: this method is renamed, search in the code, where used and change it.
        connection = self.get_connection()
        cursor = connection.cursor()

        tablename = queue['tablename']
        statement = "insert into " + tablename + "(state, payload, agent, consumer) values(:state, :payload, :agent, :consumer)"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)
        message['id'] = cursor.lastrowid
        connection.commit()
        return message

    def state(self, queue, message, state):
        # todo: this method is renamed, search in the code, where used and change it.
        connection = self.get_connection()
        cursor = connection.cursor()

        tablename = queue['tablename']
        statement = "update " + tablename + " set state=:state, message=:message, backtrace=:backtrace where id=:id"

        m = {}
        m['state'] = state
        m['message'] = Ora.iif(message, 'message', '')
        m['backtrace'] = Ora.iif(message, 'backtrace', '')
        m['id'] = message['id']

        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)
        cursor.close()
        connection.commit()

    def next(self, queue):
        connection = self.get_connection()
        cursor = connection.cursor()
        tablename = queue['tablename']
        statement = "select * from " + tablename + " where state='READY' order by created_at"
        cursor.execute(statement)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return None
        return result[0]

    def dequeue(self, claim, queue):
        try:
            claim.acquire()
            message = self.next(queue)

            if message:
                # set the state of the payload to PROCESSING
                self.state(queue, message, 'PROCESSING')

            claim.release()
            return message
        except:
            claim.release()
            raise MessageException("dequeue failed.")
