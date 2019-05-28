from harc.system.Sequence import Sequence


class JobName:

    @staticmethod
    def generate():
        identifier = '546bff91de714d828404cf77c25a4d36'
        sequence = Sequence(identifier)
        job_number = sequence.next('job_s')
        return "JOB$_{}".format(job_number)