import threading
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from typing import Dict
from typing_extensions import TypedDict
from utils.logging import IconColor, IconMode, Logger
from .zt import init as ztinit

PORT = 8766
MAGIC = 'i_am_a_net_node'.encode('utf-8')

logger = Logger('NetNode', ic=IconMode.star_filled, ic_color=IconColor.blue)

class Node(TypedDict):
    ip: str
    self: bool

nodes: TypedDict = {}

def init():
    ip = ztinit()
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((ip, PORT)) # bind to the internal network only
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    nodes[ip] = dict(ip=ip, self=True)

    def discovery_sender():
        while True:
            s.sendto(MAGIC, ('<broadcast>', PORT))
            sleep(3)

    threading.Thread(target=discovery_sender).start()

    while True:
        data, (ip, port) = s.recvfrom(1024)
        if data == MAGIC:
            if ip not in nodes:
                logger.log("New node: " + ip)
                nodes[ip] = dict(ip=ip, self=False)
