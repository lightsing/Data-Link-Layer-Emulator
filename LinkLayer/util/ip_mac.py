"""
IP MAC utils
"""
import json
from socket import *
from socket import inet_aton, inet_ntoa

from LinkLayer.error import *

with open('config.json') as reader:
    config = json.load(reader)

MAC_PREFIX = b'\x02\x00'


def get_local_ipv4_address() -> str:
    """
    Get local IPv4 Address
    :return: IPv4 Address str
    """
    test = socket(AF_INET, SOCK_DGRAM)
    test.connect((config['test']['ip'], config['test']['port']))
    ip = test.getsockname()[0]
    test.close()
    return ip


def ip2mac(ip) -> bytes:
    """
    Default IP to MAC mapping
    :param ip: IPv4 Address
    :return: MAC Address bytes
    """
    if isinstance(ip, str):
        ip_bytes = inet_aton(ip)
    elif isinstance(ip, bytes):
        if len(ip) != 4:
            raise IPv4AddressError('IPv4 address should be 4 bytes')
        ip_bytes = ip
    else:
        raise TypeError('IP should be string or bytes')
    return MAC_PREFIX + ip_bytes


def mac2ip(mac) -> str:
    """
    Default MAC to IP mapping
    :param mac: MAC Address (bytes or str)
    :return: IP str
    """
    ip_bytes = validate_mac(mac)[2:]
    return inet_ntoa(ip_bytes)


def mac_aton(mac) -> bytes:
    """
    MAC Address string to bytes
    :param mac: MAC Address String
    :return: MAC Address bytes
    """
    return validate_mac(mac)


def mac_ntoa(mac, separator=':') -> str:
    """
    MAC Address bytes to string
    :param mac: MAC Address bytes
    :param separator: separator of MAC str, default to ':'
    :return: MAC Address String
    """
    mac_string = mac.hex().upper()
    return separator.join((mac_string[i:i + 2] for i in range(0, len(mac_string), 2)))


def validate_mac(mac) -> bytes:
    if isinstance(mac, str):
        colon_split = mac.split(':')
        if len(colon_split) == 6:
            return bytes.fromhex(''.join(colon_split))
        dash_split = mac.split(':')
        if len(dash_split) == 6:
            return bytes.fromhex(''.join(dash_split))
        raise MACError('Cannot decode MAC string')
    elif isinstance(mac, bytes):
        if len(mac) == 6:
            return mac
        raise MACError('MAC address should be 6 bytes')
    else:
        raise TypeError('MAC should be string or bytes')
