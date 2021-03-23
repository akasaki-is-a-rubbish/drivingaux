import asyncio
import json

import websockets

from com.visualdust.serialthings.hub import Hub
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

hub = Hub("HUB")
hub.register(Lidar("/dev/ttyUSB0", name="RPLidar"))
# hub.register(Dist4x("/dev/ttyUSB0", 9600, name="dist4x_1"))



async def websocket_serve():
    async def client_handler(websocket, path):
        logger.log("Websocket client connected.")
        try:
            while True:
                updates = await hub.get_updates()
                obj = {}
                for name, val in updates:
                    obj[name] = val
                await websocket.send(json.dumps(obj))
        except:
            logger.log("Websocket client disconnected.")

    while len(hub.values.keys()) == 0:
        await asyncio.sleep(0.1)
    logger.log("Sensor values ready.")
    await websockets.serve(client_handler, "0.0.0.0", 8765)


async def main():
    hub.start()
    asyncio.create_task(websocket_serve())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
