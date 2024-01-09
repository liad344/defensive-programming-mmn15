import uuid


class Client:
    def __init__(self, name, public_key="", last_seen="", aes_key=""):
        self.id = uuid.uuid4()
        self.name = name
        self.public_key = public_key
        self.last_seen = last_seen
        self.aes_key = aes_key
        self.files = {}

class File:
    def __init__(self):
        self.id = uuid.uuid4()