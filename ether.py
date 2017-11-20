import json

from socket import *

from util import *


class LinkLayer:
    """
    LinkLayer class
    """

    def __init__(self, callback):
        with open('config.json') as reader:
            self.config = json.load(reader)

        self.listen = get_local_ipv4_address()
        self.MAC = ip2mac(self.listen)
        self.mac_table = dict()
        for ip in self.config['devices']:
            self.mac_table[ip2mac(ip)] = ip
        self.port = self.config['port']

        self.sock = socket(AF_INET, SOCK_DGRAM, 0)
        self.callback = callback
        self.sock.bind((self.listen, self.port))
