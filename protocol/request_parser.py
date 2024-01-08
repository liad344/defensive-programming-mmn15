import struct


# should be here?
def aes_key_request(payload):
    unpacked_data = struct.unpack('255s160s', payload)
    return unpacked_data[0], unpacked_data[1]


def registration_request(payload):
    unpacked_data = struct.unpack('255s', payload)
    return unpacked_data[0]
