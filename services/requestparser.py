import struct


class RequestParser:
    # should be here?

    def aes_key_request(self, payload):
        unpacked_data = struct.unpack('255s160s', self)
        return unpacked_data[0], unpacked_data[1]

    def registration(self, payload):
        unpacked_data = struct.unpack('255s', payload)
        return unpacked_data[0]
