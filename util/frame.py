"""
Frame Utils

Definition of Ether Frame:
+-------------+---------+---------------+
| MAC Address | Length  |    Payload    |
+-------------+---------+---------------+
|   6 bytes   | 4 bytes | 0 - 560 bytes |
+-------------+---------+---------------+

Note: the MTU of this emulator is 570 bytes.
There's no CRC in the frame.
"""
import struct
from .ip_mac import mac_aton
from error import *

MTU = 570
PAYLOAD_MTU = 560


def unpack_frame(frame: bytes) -> (bytes, bytes):
    """
    Unpacking Ether frame
    :param frame: frame bytes
    :return: mac bytes, payload bytes
    """
    if len(frame) > MTU:
        raise MTUError("Frame size should not greater than MTU")
    mac, length = struct.unpack('!6sI', frame[:10])
    payload = frame[10: 10 + length]

    return mac, payload


def pack_frame(mac, payload: bytes) -> bytes:
    """
    Packing Ether frame
    :param mac: mac address (str, bytes)
    :param payload: payload bytes
    :return: frame bytes
    """
    length = len(payload)
    if length > PAYLOAD_MTU:
        raise MTUError("Payload size Exceed MTU.")
    pass
    if isinstance(mac, str):
        mac = mac_aton(mac)
    elif isinstance(mac, bytes):
        pass
    else:
        raise TypeError('MAC should be string or bytes')

    frame = struct.pack('!6sI%ds' % length, mac, length, payload)

    return frame
