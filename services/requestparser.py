import struct

from errors import FailedParsingRequest


# todo: move to from_bytes
def registration(payload):
    try:
     unpacked = struct.unpack('255s', payload)
     return unpacked[0]
    except struct.error as e:
        raise FailedParsingRequest(e)


def aes_key_request(payload):
    try:
        unpacked_data = struct.unpack('255s160s', payload)
        return unpacked_data[0], unpacked_data[1]
    except struct.error as e:
        raise FailedParsingRequest(e)


class RequestParser:
    # should be here?

    pass


def reconnect(request):
    return None


def receive_file_request(request):
    return None