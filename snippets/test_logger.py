import logging

from harc.system.JobName import JobName
from harc.system.logger.LogConfig import LogConfig


def add(x, y):
    logger = logging.getLogger()
    job_name = JobName.generate()
    result = x + y
    logger.debug(result, extra={'job_name': job_name})
    return result


class Multiply:
    def __init__(self):
        pass

    def add(self, x, y):
        logger = logging.getLogger()
        result = x + y
        job_name = JobName.generate()
        logger.debug(result, extra={'job_name': job_name})

    def divide(self, x , y):
        logger = logging.getLogger()
        result = x / y
        job_name = JobName.generate()
        logger.info(result,extra={'job_name': job_name})

# load the log configuration rom the file log.json
LogConfig.load('log.json', 'harc')


# get the logger_ext, this done once per method
# logger_ext = LogConfig.get()

job_name = JobName.generate()
logger = logging.getLogger()
logger.debug('started', extra={'job_name': job_name})
m = Multiply()
m.add(1, 2)
m.divide(1, 2)
try:
    m.divide(1, 0)
except Exception:
    logger.exception('division by zero', extra={'job_name': job_name})
add(2, 4)
logger.info("finished", extra={'job_name': job_name})

# set the name
# format
# generate sequence number using lock
# how to log exceptions
# usage of job_names *args **kwargs





