from src.visualdust.visual.ultra_fast_lane import LaneDetector
from src.visualdust.visual.detect_service import DetectService
from src.visualdust.serialthings.dist4x import Dist4x
from utils.logger import Logger, IconMode, IconColor
from websockets.exceptions import ConnectionClosed
from src.visualdust.serialthings.lidar import Lidar
from src.visualdust.serialthings.hub import Hub
from src.visualdust.serialthings.util import *
from utils.asynchelper import loop, TaskStreamMultiplexer
import websockets
import asyncio
import json
import cv2

hub_config = json.load(open("./config/sensor.json"))
websockets_config = json.load(open("./config/websocket.json"))
vision_config = json.load(open("./config/vision.json"))

logger = Logger("Launcher", ic=IconMode.sakura, ic_color=IconColor.magenta)
logger.print_txt_file("data/com/visualdust/banner.txt").banner().print_os_info().banner()

# creating hub and register sensors
# hub = Hub.parse_config(hub_config)
hub = Hub()

# websocket server
async def websocket_serve():
    async def client_handler(websocket, path):
        logger.log("Websocket client connected.")

        task_sensors = lambda: hub.get_update()
        task_video = lambda: service.data_broadcaster.get_next()

        tasks = TaskStreamMultiplexer([task_sensors, task_video])
        
        try:
            while True:
                which_func, result = await tasks.next()
                if which_func == task_sensors:
                    name, val = result
                    await websocket.send(json.dumps({name: val}))
                elif which_func == task_video:
                    shape, data = result
                    print(shape, len(data))
                    await websocket.send(json.dumps({'image': {'w': shape[0], 'h': shape[1]}}))
                    await websocket.send(data)
        except ConnectionClosed:
            logger.log("Websocket client disconnected.")

    logger.log(f"Websocket serves at: {websockets_config['address']}"
               f":{websockets_config['port']}")
    await websockets.serve(client_handler, websockets_config["address"], websockets_config["port"])


# creating lane detector
detector = LaneDetector(vision_config)
service = DetectService(detector, cv2.VideoCapture(0))
service.start()


async def check_sensor_values():
    while len(hub.values.keys()) == 0:
        await hub.event_update.wait()
    logger.log(f"Sensor values ready")

# creating main task
async def main():
    hub.start()
    asyncio.create_task(websocket_serve())
    asyncio.create_task(check_sensor_values())


logger.log("Ready. starting to loop...")
# loop all
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
loop.run_forever()
