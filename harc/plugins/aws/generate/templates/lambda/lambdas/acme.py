from {{module}}.system.Event import Event


def lambda_handler(event, context):

    evt = Event(event)

    bucket_name = evt.get_bucket_name()
    key_name = evt.get_key_name()
    file_size = evt.get_size()

    print(bucket_name, key_name, file_size)