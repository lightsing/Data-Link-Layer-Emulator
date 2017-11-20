"""
Frame Utils

Definition of Ether Frame:
+-----------------+-----------------+---------+---------------+
| src MAC Address | dst MAC Address | length  |    payload    |
+-----------------+-----------------+-------------------------+
|     6 bytes     |     6 bytes     | 4 bytes | 0 - 560 bytes |
+-----------------+-----------------+---------+---------------+

Note: the MTU of this emulator is 576 bytes.
There's no CRC in the frame.
"""
import struct

from LinkLayer.error import *
from .ip_mac import validate_mac, mac_ntoa

MTU = 576
HEADER = 16
PAYLOAD_MTU = MTU - HEADER


class Frame:
    def __init__(self, src_mac, dst_mac, payload):
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.payload = payload

    def pack(self):
        Frame.pack_frame(self.src_mac, self.dst_mac, self.payload)

    @staticmethod
    def unpack_frame(frame: bytes) -> (bytes, bytes, bytes):
        """
        Unpacking Ether frame
        :param frame: frame bytes
        :return: mac bytes, payload bytes
        """
        if len(frame) > MTU:
            raise MTUError("Frame size should not greater than MTU")
        src_mac, dst_mac, length = struct.unpack('!6s6sI', frame[:HEADER])
        payload = frame[HEADER: HEADER + length]

        return Frame(src_mac, dst_mac, payload)

    @staticmethod
    def pack_frame(src_mac, dst_mac, payload: bytes) -> bytes:
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
        src_mac = validate_mac(src_mac)
        dst_mac = validate_mac(dst_mac)

        frame = struct.pack('!6s6sI%ds' % length, src_mac, dst_mac, length, payload)

        return frame

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'src: %(src_mac)s\n' \
               'dst: %(dst_mac)s\n' \
               'payload: %(payload)s}\n' % self.__dict__
