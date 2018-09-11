class Event(object):
    def __init__(self, event):
        self.__event = event

    def get_event(self):
        return self.__event

    def get_bucket_name(self):
        event = self.get_event()
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        return bucket_name

    def get_key_name(self):
        event = self.get_event()
        # key_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf-8'))
        key_name = event['Records'][0]['s3']['object']['key']
        return key_name

    def get_size(self):
        event = self.get_event()
        size = event['Records'][0]['s3']['object']['size']
        return size
