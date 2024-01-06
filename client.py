class Client:
    def __init__(self, id, name, publicKey, lastSeen, aesKey):
        self.id = id
        self.name = name
        self.publicKey = publicKey
        self.lastSeen = lastSeen
        self.aesKey = aesKey

        