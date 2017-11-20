import json
from socket import *

from .ip_mac import *

with open('config.json') as reader:
    config = json.load(reader)


def get_local_ipv4_address() -> str:
    test = socket(AF_INET, SOCK_DGRAM)
    test.connect((config['test']['ip'], config['test']['port']))
    ip = test.getsockname()[0]
    test.close()
    return ip


__all__ = ['get_local_ipv4_address',
           'ip2mac', 'mac2ip',
           'mac_ntoa', 'mac_aton']
