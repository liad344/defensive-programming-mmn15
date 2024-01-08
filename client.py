import uuid


class Client:
    def __init__(self, name, public_key="", last_seen="", aes_key=""):
        self.id = uuid.uuid4()
        self.name = name
        self.publicKey = public_key
        self.lastSeen = last_seen
        self.aesKey = aes_key
