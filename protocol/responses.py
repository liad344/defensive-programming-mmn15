import struct

version = 1

class ResponseHeader:
    def __init__(self, status_code, version, payload_size):
        self.status_code = status_code
        self.version = version
        self.payload_size = payload_size


class Response:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self.payload = payload

        payload_size = len(self.payload)
        self.response_header = ResponseHeader(self.status_code, version, payload_size)

    def __str__(self):
        return "status code {}, payload {}".format(self.status_code, self.payload)

    def encode(self):
        pass


class SuccessResponse(Response):
    def __init__(self, client_id):
        super().__init__(1600, payload=bytes(client_id))

class FailedResponse(Response):
    def __init__(self):
        super().__init__(1601, payload=bytes(None))

class SendAESKeyResponse(Response):
    def __init__(self, client_id, aes_key):
        super().__init__(1602, payload=bytes(client_id,aes_key))

class CRCValidResponse(Response):
    def __init__(self, client_id, content_size, file_name, cksum):
        super().__init__(1603,payload=bytes(client_id,content_size,file_name,cksum))
class OkResponse(Response):
    def __init__(self, client_id):
        super().__init__(1604,payload=bytes(client_id))
class ReconnectResponse(Response):
    def __init__(self, client_id, aes_key):
        super().__init__(1605,payload=bytes(client_id,aes_key))
class ReconnectFailedResponse(Response):
    def __init__(self, client_id):
        super().__init__(1606,payload=bytes(client_id))
class GeneralErrorResponse(Response):
    def __init__(self, error):
        super().__init__(1607,payload=bytes(error))

