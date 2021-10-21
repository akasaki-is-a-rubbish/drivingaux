import json
import threading
import time
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from typing import Dict
from typing_extensions import TypedDict
from utils.asynchelper import Broadcaster, Event
from utils.logging import IconColor, IconMode, Logger
from .zt import init as ztinit

PORT = 8766
MAGIC = 'i_am_a_net_node'.encode('utf-8')
HEARTBEAT_INTERVAL = 3

logger = Logger('NetNode', ic=IconMode.star_filled, ic_color=IconColor.blue)

class Node(TypedDict):
    ip: str
    name: str
    self: bool
    last_active: float

nodes: Dict[str, Node] = {}

on_nodes_update = Event()

def get_nodes():
    return nodes

def init(node_name):
    ip = ztinit()
    if ip is None:
        return
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((ip, PORT)) # bind to the internal network only
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    nodes[ip] = dict(ip=ip, self=True, last_active=0, node_name=node_name)

    broadcast_data = MAGIC + json.dumps({'name': node_name}).encode('utf-8')

    def timer():
        while True:
            # Broadcast the magic packet
            s.sendto(broadcast_data, ('<broadcast>', PORT))
            sleep(HEARTBEAT_INTERVAL)

            # Find and remove dead nodes
            now = time.time()
            for ip in [*nodes.keys()]:
                if nodes[ip]['self'] == False and now - nodes[ip]['last_active'] > HEARTBEAT_INTERVAL * 2:
                    logger.log("Removed node: " + ip)
                    del nodes[ip]
                    on_nodes_update.set_and_clear_threadsafe()

    def receiver():
        while True:
            data, (ip, port) = s.recvfrom(1024)
            if data.startswith(MAGIC):
                if ip not in nodes:
                    logger.log("New node: " + ip)
                    payload = json.loads(data[len(MAGIC):].decode('utf-8'))
                    nodes[ip] = dict(ip=ip, self=False, name=payload['name'])
                    on_nodes_update.set_and_clear_threadsafe()
                nodes[ip]['last_active'] = time.time()

    threading.Thread(target=timer).start()
    receiver()
