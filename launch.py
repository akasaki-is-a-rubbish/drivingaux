from com.visualdust.visual.ultra_fast_lane import LaneDetector
from com.visualdust.serialthings.dist4x import Dist4x
from utils.logger import Logger, IconMode, IconColor
from websockets.exceptions import ConnectionClosed
from com.visualdust.serialthings.lidar import Lidar
from com.visualdust.serialthings.hub import Hub
from utils.asynchelper import loop
from utils.util import *
import websockets
import asyncio
import json

sensor_config = json.load(open("./config/sensor.json"))
websockets_config = json.load(open("./config/websocket.json"))
vision_config = json.load(open("./config/vision.json"))

logger = Logger("Launcher", ic=IconMode.sakura, ic_color=IconColor.magenta)
print_txt(open("./res/banner.txt"))
logger.banner().print_os_info().banner()


def parse_dict(config, name=None):
    if config["type"] == Dist4x.__name__:
        return Dist4x(config["port"], config["baudrate"], name)
    if config["type"] == Lidar.__name__:
        return Lidar(config["port"], name)


def parse_all(config_for_all):
    result = []
    for item in config_for_all:
        result.append(parse_dict(config_for_all[item], name=item))
    return result


def parse_file(config_file):
    if type(config_file) == str:
        config_file = open(config_file)
    configs = json.load(config_file)
    return parse_all(configs)


# creating hub and register sensors
hub = Hub("HUB")
for sensor in parse_all(sensor_config):
    hub.register(sensor)


# hub.register(Lidar("/dev/ttyUSB4", name="RPLidar")) \
#     .register(Dist4x("/dev/ttyUSB0", 9600, name="dist4x_0")) \
#     .register(Dist4x("/dev/ttyUSB1", 9600, name="dist4x_1")) \
#     .register(Dist4x("/dev/ttyUSB2", 9600, name="dist4x_2")) \
#     .register(Dist4x("/dev/ttyUSB3", 9600, name="dist4x_3")) \
#     # hub.register(Dist4x("/dev/ttyUSB0", 9600, name="dist4x_1"))

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
