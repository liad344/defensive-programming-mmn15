import logging
import sqlite3

import client
import errors
import services
import protocol
import socket
import selectors

from client import Client
from protocol import responses
from services.requestparser import registration

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
        self.crypto_service = services.mycrypto("name")
        self.port = readConfigFile()
        self.host = "0.0.0.0"
        self.logger = logging.getLogger('server_logger')
        self.clients = self.db_service.load_clients()
        self.parser = services
        self.selector = selectors.DefaultSelector()

    def update_client(self, name, aes_key, public_key):
        self.db_service.update_client(name, aes_key, public_key)

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
        match request.header.code:
            case 1025:
                try:
                    parsed = services.requestparser.registration(request)
                    self.register_new_user(parsed)
                except errors.FailedParsingRequest as e:
                    self.logger.warning(e)
            case 1026:
                try:
                    name, key = services.requestparser.aes_key_request(request)
                    self.receive_public_key(name, key)
                except errors.FailedParsingRequest as e:
                    self.logger.warning(e)

            case 1027:
                try:
                    name = services.requestparser.reconnect(request)
                    self.reconnect(name)
                except errors.FailedParsingRequest as e:
                    self.logger.warning(e)

            case 1028:
                try:
                    content_size, og_file_size, packet_num, total_packets, file_name, file_content = (
                     services.requestparser.receive_file_request(request))
                    self.receive_file(request.header.client_id, content_size, og_file_size, packet_num,
                     total_packets, file_name, file_content)
                except errors.FailedParsingRequest as e:
                    self.logger.warning(e)
            case 1029:
                try:
                    pass
                except errors.FailedParsingRequest as e:
                    self.logger.warning(e)
            case 1030:
                try:
                    pass
                except errors.FailedParsingRequest as e:
                    self.logger.warning(e)

    def register_new_user(self, payload):
        new_client_name = str(payload)
        client = Client(name=new_client_name)
        for client_id, client in self.clients.items():
            if client.name == new_client_name:
                self.send_response(responses.FailedResponse)
                return

        self.db_service.add_client(client)
        self.clients[client.id] = client
        self.send_response(responses.SuccessResponse)

    def receive_public_key(self, name, public_key):
        client_id = name # todo: get real id
        aes_key = self.crypto_service.generate_aes_key()
        self.crypto_service.encrypt_with_public_key(aes_key, public_key)
        self.update_client(name, aes_key, public_key)

        response = responses.SendAESKeyResponse(client_id, aes_key)
        self.send_response(response.payload)
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
