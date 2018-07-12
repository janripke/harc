from harc.repositories.MessageRepository import MessageRepository
from harc.connectors.DatasourceBuilder import DatasourceBuilder
from harc.repositories.QueueRepository import QueueRepository
import json


class Message:
    def __init__(self):
        pass

    @staticmethod
    def enqueue(queue_name, payload, agent,  consumer):
        # todo: this method is renamed, search in the code, where used and change it. the parameter queue is added
        harc = DatasourceBuilder.find('harc-ds')
        queue_repository = QueueRepository(harc)
        queue = queue_repository.find_by_name(queue_name)

        queue_ds = DatasourceBuilder.find(queue['datasource'])
        message_repository = MessageRepository(queue_ds)

        message = {}
        message['state'] = 'READY'
        message['payload'] = json.dumps(payload)
        message['agent'] = agent
        message['consumer'] = consumer
        result = message_repository.insert(queue, message)
        message_repository.close()

        return result
