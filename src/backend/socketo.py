from utils.logging import Logger, IconMode, IconColor
from websockets.exceptions import ConnectionClosed
from src.visualdust.visual.cam_noneblocking import CameraThreadoo
from utils.asynchelper import TaskStreamMultiplexer
import websockets
import time
import json
import numpy as np
import cv2


# websocket server
async def websocket_serve(hub, detect_service, camera_service: CameraThreadoo, target_service, config):
    logger = Logger("Websocket", ic=IconMode.star, ic_color=IconColor.magenta)

    async def client_handler(websocket: websockets.WebSocketServerProtocol, path):
        logger.log("Websocket client connected.")

        image_requested = False

        task_recv = lambda: websocket.recv()
        task_sensors = lambda: hub.get_update()
        task_video = lambda: camera_service.frames_broadcaster['fronting'].get_next_with_seq()
        task_points = lambda: detect_service.data_broadcaster.get_next()
        task_targets = lambda: target_service.data_broadcaster.get_next()
        tasks = TaskStreamMultiplexer([task_recv, task_sensors, task_video, task_points, task_targets])

        try:
            # Client handler event loop:
            while True:
                which_func, result = await tasks.next()
                if which_func == task_recv:
                    obj = json.loads(result)
                    if obj['cmd'] == 'requestImage':
                        image_requested = True
                elif which_func == task_sensors:
                    name, val = result
                    await websocket.send(json.dumps({name: val}))
                elif which_func == task_video:
                    # if image_requested == False:
                    #     continue
                    image_requested = False
                    seq, image = result
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    shape = image.shape
                    buffer = image.tobytes("C")
                    await websocket.send(json.dumps({'image': {'w': shape[1], 'h': shape[0], 'seq': seq}}))
                    await websocket.send(buffer)
                elif which_func == task_points:
                    data = json.dumps({'lanePoints': [{'x': x, 'y': y} for [x, y] in result]})
                    await websocket.send(data)
                elif which_func == task_targets:
                    await websocket.send(json.dumps({'targets': result}))

        except ConnectionClosed:
            logger.log("Websocket client disconnected.")

    logger.log(f"Websocket serves at: {config['address']}"
               f":{config['port']}")
    await websockets.serve(client_handler, config["address"], config["port"], compression=None)
