import json
import threading
from random import random
from socket import *

from LinkLayer.util import *


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
            frame = Frame.unpack_frame(frame)
            if frame.src_mac not in self.link_layer.mac_table:
                self.link_layer.mac_table[frame.src_mac] = address[0]
            # calling callback
            self.link_layer.callback(frame)

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

        self.income_handler = IncomeHandler(self)
        self.income_handler.start()

    def sendto(self, dst_mac, payload: bytes, src_mac=None):
        """
        Sending ether frame
        :param dst_mac: destination mac address
        :param payload: payload bytes
        :return: None
        """
        if random() < self.config['loss']:
            # drop frame
            return
        if src_mac is None:
            src_mac = self.MAC
        frame = Frame.pack_frame(src_mac, dst_mac, payload)
        if dst_mac in self.mac_table:
            self.sock.sendto(frame, (self.mac_table[dst_mac], self.port))
        else:
            # flood
            for _, ip in self.mac_table.items():
                self.sock.sendto(frame, (ip, self.port))
