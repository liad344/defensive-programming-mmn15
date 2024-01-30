import logging
import sqlite3

import client
import services
import protocol
import socket
import selectors

from client import Client
from protocol import responses

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
        self.db_service = services.Db("name")
        self.crypto_service = services.Crypto("name")
        self.port = readConfigFile()
        self.host = "0.0.0.0"
        self.logger = logging.getLogger('server_logger')
        self.clients = self.db_service.load_clients()
        self.parser = services.RequestParser()
        self.selector = selectors.DefaultSelector()

    def update_client(self, name, aes_key, public_key):
        self.db_service.update_client(name, aes_key, public_key)

        # todo: decide if clients is by id or by name- unclear from assignment
        self.clients[name].aes_key = aes_key
        self.clients[name].public_key = public_key

    def send_response(self, response):
        pass

    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Socket should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self.selector.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        with conn:
            header_bytes = conn.recv(HeaderSize)
            if header_bytes:
              header = protocol.RequestHeader.from_bytes(header_bytes)
              payload = conn.recv(header.payload_size)
              req = protocol.Request(header, payload)
              if req is not None:
                self.request_router(req)
            else:
              print('closing', conn)
              self.selector.unregister(conn)
              conn.close()

    def listen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        s.setblocking(False)
        self.selector.register(s, selectors.EVENT_READ, self.accept)
        try:
            while True:
                events = self.selector.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
        finally:
            s.close()
    def request_router(self, request):
        print("in req router")
        match request.header.code:
            case 1025:
                # todo: error handling
                parsed = self.parser.registration(request)
                self.register_new_user(parsed)
            case 1026:
                name, key = self.parser.aes_key_request(request)
                self.receive_public_key(name, key)
            case 1027:
                name = self.parser.reconnect(request)
                self.reconnect(name)
            case 1028:
                # todo: error handling reading client id
                content_size, og_file_size, packet_num, total_packets, file_name, file_content = (
                    self.parser.receive_file_request(request))
                self.receive_file(request.header.client_id, content_size, og_file_size, packet_num,
                                  total_packets, file_name, file_content)
            case 1029:
                pass
            case 1030:
                pass

    def register_new_user(self, payload):
        new_client_name = "todo parse paylod"
        client = Client(name=new_client_name)
        for client_id, client in self.clients.items():
            if client.name == new_client_name:
                self.send_response(responses.FailedResponse)
                return

        self.db_service.add_client(client)
        self.clients[client.id] = client
        self.send_response(responses.SuccessResponse)

    def receive_public_key(self, name, public_key):
        aes_key = self.crypto_service.generate_aes_key()
        self.crypto_service.encrypt_with_public_key(aes_key, public_key)
        self.update_client(name, aes_key, public_key)
        self.send_response(responses.SendAESKeyResponse)
        pass

    def reconnect(self, name):
        if self.clients[name] != "":
            self.send_response(responses.SuccessResponse)
        else:
            self.send_response(responses.FailedResponse)

    def receive_file(self, client_id, content_size, og_file_size, packet_num,
                     total_packets, file_name, file_content):

        file = client.File()
        self.clients[client_id].files[file_name] = og_file_size

        aes_key = self.clients[client_id].aes_key
        decrypted = self.crypto_service.decrypt(file_content, aes_key)

        try:
            with open(f"./{file_name}", 'r') as file:
                bytes_written = file.write(decrypted)

        except FileNotFoundError:
            print("File not found.")
        pass
