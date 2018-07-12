import time
from harc.connectors.DatasourceBuilder import DatasourceBuilder
from harc.repositories.JobRepository import JobRepository
from harc.system.logger.Logger import Logger
from harc.system.Traceback import Traceback


class WatchWorker(object):
    def __init__(self, watcher, settings, threads, abort):
        object.__init__(self)
        self.__watcher = watcher
        self.__settings = settings
        self.__threads = threads
        self.__abort = abort
        self.__running = True

    def get_watcher(self):
        return self.__watcher

    def get_settings(self):
        return self.__settings

    def get_threads(self):
        return self.__threads

    def get_abort(self):
        return self.__abort

    def is_running(self):
        return self.__running

    def running(self, running):
        self.__running = running

    def run(self):
        abort = self.get_abort()
        harc = DatasourceBuilder.build('harc-ds.json')
        logger = Logger(self)
        job_repository = JobRepository(harc)
        job = job_repository.job()
        job_name = job['job_name']
        job_repository.close()
        settings = self.get_settings()
        threads = self.get_threads()
        while self.is_running():
            try:

                watcher = self.get_watcher()
                watcher.watch(settings, threads, abort)

                # check if we need to abort, can be called from the main thread or other thread
                aborted = abort.is_aborted()
                self.running(not aborted)

                time.sleep(settings['watcher_idle_delay'])

            except:
                aborted = abort.is_aborted()
                self.running(not aborted)

                result = Traceback.build()
                logger.fatal(job_name, result['message'], result['backtrace'])
                time.sleep(settings['worker_exception_delay'])
