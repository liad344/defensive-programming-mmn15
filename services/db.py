import sqlite3

from client import Client


class Db:
    def __init__(self, name):
        self.name = name
        self.db = sqlite3.connect("defensive.db")
        self.init_tables()

    def init_tables(self):
        # todo: check if already exsist, if so dont load
        cursor = self.db.cursor()
        sql = '''
        CREATE TABLE clients (
            ID TEXT PRIMARY KEY,
            Name TEXT,
            PublicKey TEXT,
            LastSeen DATETIME,
            AESKey TEXT
        );
        '''
        try:
            cursor.execute(sql)
        except sqlite3.OperationalError as e:
            if "already exists" in str(e):
                print(e)

        self.db.commit()

    def load_clients(self):
        # Create a cursor object
        cursor = self.db.cursor()

        # SQL query to fetch all clients
        query = "SELECT ID, Name, PublicKey, LastSeen, AESKey FROM clients"

        # Execute the query
        cursor.execute(query)

        # Create a dictionary to store clients
        clients = {}

        # Iterate over query results
        for row in cursor.fetchall():
            # Create a Client object and add it to the dictionary
            client = Client(id=row[0], name=row[1], publicKey=row[2], lastSeen=row[3], aesKey=row[4])
            clients[client.id] = client

        return clients

    def add_client(self, client):
        # todo: move to server utils
        cursor = self.db.cursor()
        query = '''INSERT INTO clients (ID, Name, PublicKey, LastSeen, AESKey) 
                      VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(query,
                       (client.id, client.name, client.public_key, client.last_seen, client.aes_key))

    def update_client(self, name, aes_key, public_key):
        return ""