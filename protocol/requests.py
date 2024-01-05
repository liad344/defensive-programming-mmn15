import struct


class RequestHeader:
    def __init__(self, client_id, code, version, payload_size):
        self.status_code = code
        self.version = version
        self.payload_size = payload_size
        self.client_id = client_id

    @classmethod
    def from_bytes(cls, data):
        # Unpack the data
        # Format string: '16sBHI' -> 16-char string, 1-byte uint, 2-byte uint, 4-byte uint
        unpacked_data = struct.unpack('16sBHI', data)

        # TODO: check this line out, pretty sure its ASCII with different ternintion
        # Process the ClientId to remove null bytes and convert to a string
        client_id = unpacked_data[0].decode('utf-8').rstrip('\x00')

        # Remaining fields
        version = unpacked_data[1]
        code = unpacked_data[2]
        payload_size = unpacked_data[3]

        return cls(client_id, version, code, payload_size)


class Request:
    def __init__(self, header, payload):
        self.header = header
        self.payload = payload


class RegistrationRequest(Request):
    def __init__(self, client_id, version, name):
        super().__init__(client_id, 1025, version, payload=bytes(name))


class SendPublicKeyRequest(Request):
    def __init__(self, client_id, version, name):
        super().__init__(client_id, 1026, version, payload=bytes(name))


class ReconnectRequest(Request):
    def __init__(self, client_id, version, name):
        super().__init__(client_id, 1027, version, payload=bytes(name))


class SendFileRequest(Request):
    def __init__(self, client_id, version, name):
        super().__init__(client_id, 1028, version, payload=bytes(name))


class CRCValidRequest(Request):
    def __init__(self, client_id, version, name):
        super().__init__(client_id, 1029, version, payload=bytes(name))


class CRCNotValidRequest(Request):
    def __init__(self, client_id, version, name):
        super().__init__(client_id, 1030, version, payload=bytes(name))


class CRCNotValidFinalTimeRequest(Request):
    def __init__(self, client_id, version, name):
        super().__init__(client_id, 1031, version, payload=bytes(name))
