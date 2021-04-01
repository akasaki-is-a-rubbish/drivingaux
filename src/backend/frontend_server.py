from utils.logging import Logger, IconMode, IconColor
from websockets.exceptions import ConnectionClosed
from src.visualdust.visual.cam_noneblocking import CameraThreadoo
from utils.asynchelper import TaskStreamMultiplexer
import websockets
import json
import numpy as np

# websocket server
async def websocket_serve(hub, detect_service, camera_service: CameraThreadoo, config):
    logger = Logger("Websocket", ic=IconMode.star, ic_color=IconColor.magenta)
    async def client_handler(websocket, path):
        logger.log("Websocket client connected.")

        task_sensors = lambda: hub.get_update()
        task_video = lambda: camera_service.get_next('fronting')
        task_points = lambda: detect_service.data_broadcaster.get_next()
        tasks = TaskStreamMultiplexer([task_sensors, task_video, task_points])
        
        try:
            while True:
                which_func, result = await tasks.next()
                if which_func == task_sensors:
                    name, val = result
                    await websocket.send(json.dumps({name: val}))
                elif which_func == task_video:
                    image: np.ndarray = result
                    shape, buffer = image.shape, image.tobytes("C")
                    # print(shape, len(buffer))
                    await websocket.send(json.dumps({'image': {'w': shape[1], 'h': shape[0]}}))
                    await websocket.send(buffer)
                elif which_func == task_points:
                    data = json.dumps({'frontPoints': [{'x': x, 'y': y} for [x, y] in result]})
                    # print(result, j)
                    await websocket.send(data)
        except ConnectionClosed:
            logger.log("Websocket client disconnected.")

    logger.log(f"Websocket serves at: {config['address']}"
               f":{config['port']}")
    await websockets.serve(client_handler, config["address"], config["port"])