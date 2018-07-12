import time
from harc.connectors.DatasourceBuilder import DatasourceBuilder
from harc.executors.ManagedWorker import ManagedWorker
from harc.repositories.MessageRepository import MessageRepository
from harc.system.ClassLoader import ClassLoader
from harc.system.logger.Logger import Logger
from harc.system.Traceback import Traceback


class MessageWorker(ManagedWorker):
    def __init__(self, id, settings, claim, abort, stop):
        ManagedWorker.__init__(self, id, settings, claim, abort, stop)

    def run(self, queue):
        abort = self.get_abort()
        claim = self.get_claim()
        stop = self.get_stop()
        settings = self.get_settings()
        logger = Logger(self)
        job_name = ''
        message = None
        while self.is_running():
            try:
                job_name = ''
                message = None
                logger = Logger(self)
                # retrieve the next message
                datasource = queue['datasource']
                queue_ds = DatasourceBuilder.find(datasource)
                message_repository = MessageRepository(queue_ds)
                message = message_repository.dequeue(claim, queue)

                if message:

                    consumer = ClassLoader.find(message['consumer'])
                    consumer.action(message)

                    message_repository.state(queue, message, 'PROCESSED')

                # no message to process
                if not message:
                    time.sleep(settings['worker_idle_delay'])

                # check if we need to abort, can be called from the main thread or other thread
                aborted = abort.is_aborted()
                self.running(not aborted)

                # check if we need to stop, will be set by the agent's WatchWorker thread
                if not aborted:
                    stopped = stop.is_stopped()
                    self.running(not stopped)

                logger.trace(job_name, 'worker #' + str(self.get_id()) + " executed.")

            except:
                aborted = abort.is_aborted()
                self.running(not aborted)

                if not aborted:
                    stopped = stop.is_stopped()
                    self.running(not stopped)

                result = Traceback.build()
                if message:
                    try:
                        datasource = queue['datasource']
                        queue_ds = DatasourceBuilder.find(datasource)
                        message_repository = MessageRepository(queue_ds)
                        result['id'] = message['id']
                        message_repository.state(queue, result, 'FAILED')
                        message_repository.close()
                    except:
                        logger.fatal(job_name, 'Failed to persist message failure')

                logger.fatal(job_name, result['message'], result['backtrace'])
                time.sleep(settings['worker_exception_delay'])

