"""
IP MAC utils
"""
import json
from socket import *

from socket import inet_aton, inet_ntoa

with open('config.json') as reader:
    config = json.load(reader)


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

def ip2mac(ip) -> str:
    """
    Default IP to MAC mapping
    :param ip: IPv4 Address
    :return: MAC Address String
    """
    if isinstance(ip, str):
        ip_bytes = inet_aton(ip)
    elif isinstance(ip, bytes):
        ip_bytes = ip
    else:
        raise TypeError('IP should be string or bytes')
    return mac_ntoa(b'\xff\xff' + ip_bytes)


def mac2ip(mac) -> str:
    """
    Default MAC to IP mapping
    :param mac: MAC Address (bytes or str)
    :return: IP String
    """
    if isinstance(mac, str):
        ip_bytes = bytes.fromhex(''.join(mac.split(':')[2:]))
    elif isinstance(mac, bytes):
        ip_bytes = mac[2:]
    else:
        raise TypeError('MAC should be string or bytes')
    return inet_ntoa(ip_bytes)


def mac_aton(mac) -> bytes:
    """
    MAC Address string to bytes
    :param mac: MAC Address String
    :return: MAC Address bytes
    """
    return bytes.fromhex(''.join(mac.split(':')))


def mac_ntoa(mac) -> str:
    """
    MAC Address bytes to string
    :param mac: MAC Address bytes
    :return: MAC Address String
    """
    mac_string = mac.hex().upper()
    return ':'.join((mac_string[i:i + 2] for i in range(0, len(mac_string), 2)))
