import logging
import sqlite3

import protocol
import socket

from client import Client
from protocol import responses
from request_handlers import registration, _CRC_not_ok, _CRC_ok, recive_file, reconnect, receive_public_key

#  Protocol V0.0
#
#  ClientId(16 str) | Version(1 uint) | Code(2 uint) | PayloadSize(4 uint) | Payload(variable)
#
#

HeaderSize = 16 + 1 + 2 + 4


def readConfigFile():
    return 1009


class Server:

    # todo: Add shutdown and clode all tcp/db connections
    def __init__(self):
        self.port = readConfigFile()
        self.host = "0.0.0.0"
        self.logger = logging.getLogger('server_logger')
        self.db = sqlite3.connect("defensive.db")
        self.init_tables()
        self.clients = self.load_client_from_db()

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
        cursor.execute(sql)
        self.db.commit()

    def read_requests(self, conn) -> protocol.Request:
        try:
            header_bytes = conn.recv(HeaderSize)
            header = protocol.RequestHeader.from_bytes(header_bytes)
            payload = conn.recv(header.payload_size)
            return protocol.Request(header, payload)

        except Exception as e:
            self.logger.error(e)

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    request = self.read_requests(conn)
                    self.request_router(request)

    def request_router(self, request):
        match request.header.code:
            case 1025:
                registration(request.payload)
            case 1026:
                receive_public_key()
            case 1027:
                reconnect()
            case 1028:
                recive_file()
            case 1029:
                _CRC_ok()
            case 1030:
                _CRC_not_ok()

    def load_client_from_db(self):
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

    def registration(self, payload):
        #todo: parse payload, should be string name
        name = "todo parse paylod"
        for client_id, client in self.clients.items():
            if client.name == name:
                return responses.FailedResponse
            else:
                self.add_client(client)

    def add_client(self, client):
        pass
        


