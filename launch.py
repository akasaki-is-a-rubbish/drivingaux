from com.visualdust.visual.ultra_fast_lane import LaneDetector
from com.visualdust.serialthings.dist4x import Dist4x
from utils.logger import Logger, IconMode, IconColor
from websockets.exceptions import ConnectionClosed
from com.visualdust.serialthings.lidar import Lidar
from com.visualdust.serialthings.hub import Hub
from com.visualdust.serialthings.util import *
from utils.asynchelper import loop
import websockets
import asyncio
import json

hub_config = json.load(open("./config/sensor.json"))
websockets_config = json.load(open("./config/websocket.json"))
vision_config = json.load(open("./config/vision.json"))

logger = Logger("Launcher", ic=IconMode.sakura, ic_color=IconColor.magenta)
logger.print_txt_file("data/com/visualdust/banner.txt").banner().print_os_info().banner()

# creating hub and register sensors
hub = Hub.parse_config(hub_config)

# websocket server
async def websocket_serve():
    async def client_handler(websocket, path):
        logger.log("Websocket client connected.")
        await websocket.send("OK")
        try:
            while True:
                name, val = await hub.get_update()
                await websocket.send(json.dumps({name: val}))
        except ConnectionClosed:
            logger.log("Websocket client disconnected.")

    while len(hub.values.keys()) == 0:
        await asyncio.sleep(0.3)
    logger.log(f"Websocket started to serve at: {websockets_config['address']}"
               f":{websockets_config['port']}")
    await websockets.serve(client_handler, websockets_config["address"], websockets_config["port"])


# creating lane detector
detector = LaneDetector(vision_config)


# creating main task
async def main():
    hub.start()
    asyncio.create_task(websocket_serve())


logger.log("Ready. starting to loop...")
# loop all
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
loop.run_forever()
