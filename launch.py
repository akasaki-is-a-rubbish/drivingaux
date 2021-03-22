import asyncio
import json

import websockets

from com.visualdust.serialthings.hub import Hub, SensorValue as SValues
from com.visualdust.serialthings.lidar import Lidar
from utils.logger import Logger
from utils.util import *

"""
Prehooks
"""
sensor_config = json.load(open("./config/sensor.json"))
websockets_config = json.load(open("./config/websocket.json"))
vision_config = json.load(open("./config/vision.json"))

logger = Logger("Launcher")
print_txt(open("./res/banner.txt"))
logger.banner().print_os_info().banner()

# d4x_1 = Dist4x("/dev/ttyUSB0", 9600, "dist4x_1")
lidar = Lidar("/dev/ttyUSB0", name="RPLidar")
hub = Hub("HUB").register(lidar)


async def client_handler(websocket, path):
    logger.log("Client handler started.")
    try:
        while True:
            await websocket.send(json.dumps(SValues))
            await asyncio.sleep(0.1)
    except:
        logger.log("Client seems disconnected. Ignored.")


async def socket_serve():
    while len(SValues.keys()) == 0:
        await asyncio.sleep(0.1)
    logger.log("Sensor values ready. Starting to serve at: 0.0.0.0:8765")
    await websockets.serve(client_handler, "0.0.0.0", 8765)


async def main():
    hub.start()
    asyncio.create_task(socket_serve())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
