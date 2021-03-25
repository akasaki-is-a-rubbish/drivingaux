from src.visualdust.visual.ultra_fast_lane import LaneDetector
from src.visualdust.visual.detect_service import DetectService
from src.visualdust.serialthings.dist4x import Dist4x
from utils.logger import Logger, IconMode, IconColor
from websockets.exceptions import ConnectionClosed
from src.visualdust.serialthings.lidar import Lidar
from src.visualdust.serialthings.hub import Hub
from src import frontend_server
from src.visualdust.serialthings.util import *
from utils.asynchelper import loop, TaskStreamMultiplexer
import websockets
import asyncio
import json
import cv2

# websocket server
async def websocket_serve(hub, detect_service, config):
    logger = Logger("Websocket", ic=IconMode.star, ic_color=IconColor.magenta)
    async def client_handler(websocket, path):
        logger.log("Websocket client connected.")

        task_sensors = lambda: hub.get_update()
        task_video = lambda: detect_service.data_broadcaster.get_next()

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

    logger.log(f"Websocket serves at: {config['address']}"
               f":{config['port']}")
    await websockets.serve(client_handler, config["address"], config["port"])