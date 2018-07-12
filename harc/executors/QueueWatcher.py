from harc.connectors.DatasourceBuilder import DatasourceBuilder
from harc.executors.MessageWorker import MessageWorker
from harc.repositories.QueueRepository import QueueRepository
from harc.threading.Runner import Runner
from harc.threading.Stop import Stop
from harc.threading.Claim import Claim


class QueueWatcher(object):
    def __init__(self):
        object.__init__(self)

    def watch(self, settings, threads, abort):
        harc = DatasourceBuilder.build('harc-ds.json')
        queue_repository = QueueRepository(harc)
        queues = queue_repository.list()
        for queue in queues:
            if not threads.has_group(queue['hashcode']) and queue['active'] == '1':
                stop = Stop()
                claim = Claim()
                pool_size = settings['pool_size']
                for i in range(0, pool_size):
                    id = threads.next_id()
                    t = Runner.run(MessageWorker(id, settings, claim, abort, stop), queue)
                    threads.append({'id': id, 'group': queue['hashcode'], 'thread': t, 'stop': stop})
            if threads.has_group(queue['hashcode']) and queue['active'] == '0':
                stop = threads.list_by_group(queue['hashcode'])[0]['stop']
                stop.stopped(True)
                threads.remove_by_group(queue['hashcode'])
        queue_repository.close()
