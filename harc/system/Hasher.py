import hashlib
import uuid


class Hasher:
    def __init__(self):
        pass

    @staticmethod
    def sha256():
        sha256 = hashlib.sha256()
        sha256.update(uuid.uuid4().hex.encode('utf-8'))
        return sha256.hexdigest()
