import json
import threading
from socket import *

from util import *


class IncomeHandler(threading.Thread):
    def __init__(self, link_layer):
        super(IncomeHandler, self).__init__()
        self.link_layer = link_layer

    def run(self):
        while True:
            frame, address = self.link_layer.sock.recvfrom(MTU)
            if address[1] != self.link_layer.config['port']:
                # ignore any non common port
                continue
            mac, payload = unpack_frame(frame)
            if mac not in self.link_layer.mac_table:
                self.link_layer.mac_table[mac] = address[0]
            # calling callback
            self.link_layer.callback(payload)

class LinkLayer:
    """
    LinkLayer class
    """

    def __init__(self, callback, MAC=None):
        with open('config.json') as reader:
            self.config = json.load(reader)

        self.listen = get_local_ipv4_address()
        if MAC is not None:
            self.MAC = MAC
        else:
            self.MAC = ip2mac(self.listen)
        self.mac_table = dict()
        for ip in self.config['devices']:
            self.mac_table[ip2mac(ip)] = ip
        self.port = self.config['port']

        self.sock = socket(AF_INET, SOCK_DGRAM, 0)
        self.callback = callback
        self.sock.bind((self.listen, self.port))
