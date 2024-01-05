import logging

import protocol
import socket

#  Protocol V0.0
#
#  ClientId(16 str) | Version(1 uint) | Code(2 uint) | PayloadSize(4 uint) | Payload(variable)
#
#

HeaderSize = 16 + 1 + 2 + 4


def readConfigFile():
    return 1009


class Server:
    def __init__(self):
        self.port = readConfigFile()
        self.host = "0.0.0.0"
        self.logger = logging.getLogger('server_logger')

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

    def request_router(self, code):
        match code:
            case 1025:
                self.registration()
            case 1026:
                self.receive_public_key()
            case 1027:
                self.reconnect()
            case 1028:
                self.recive_file()
            case 1029:
                self._CRC_ok()
            case 1030:
                self._CRC_not_ok()

    def registration(self):
        pass

    def receive_public_key(self):
        pass

    def reconnect(self):
        pass

    def recive_file(self):
        pass

    def _CRC_not_ok(self):
        pass

    def _CRC_ok(self):
        pass
