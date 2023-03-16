import requests
from utils.logging import Logger, IconMode, IconColor
from websockets.exceptions import ConnectionClosed
from src.visualdust.visual.cam_noneblocking import CameraService
from src.visualdust.visual.visual_model_service import *
from src.backend.node import get_nodes, on_nodes_update
from utils.asynchelper import TaskStreamMultiplexer
import websockets
import time
import json
import numpy as np
import cv2

config_id = json.load(open("config/id.json", "r"))["encryptedId"]

print("config_id", config_id)

# websocket server
async def websocket_serve(
    hub,
    lane_detect_service: LaneDetectService,
    camera_service: CameraService,
    target_service: TargetDetectService,
    segmentation_provider: SegmentationService,
    config,
):
    logger = Logger("Websocket", ic=IconMode.star, ic_color=IconColor.magenta)
    """
    @:param websocket connected with frontend
    using sync io
    """

    async def client_handler(websocket: websockets.WebSocketServerProtocol, path):
        logger.log("Websocket client connected.")

        # Client state
        image_enabled = False
        image_requested = False

        # the recieved task
        task_recv = lambda: websocket.recv()
        # waiting for sensor update
        task_sensors = lambda: hub.get_update()
        # captured frame
        task_video = lambda: camera_service.frames_broadcaster[
            "camera_video"
        ].get_next_with_seq()
        # waiting for detection service result
        task_points = lambda: lane_detect_service.data_broadcaster.get_next()
        # waiting for segmentation provider result
        task_imgseg = lambda: segmentation_provider.data_broadcaster.get_next()
        # waiting for lane detection result
        task_targets = lambda: target_service.data_broadcaster.get_next()
        # waiting for nodes change
        task_nodes = lambda: on_nodes_update.wait()

        tasks = TaskStreamMultiplexer(
            [
                task_recv,
                task_sensors,
                task_points,
                task_targets,
                task_imgseg,
                task_video,
                task_nodes,
            ]
        )

        async def send_nodes():
            await websocket.send(json.dumps({"nodes": [*get_nodes().values()]}))

        async def handle_request(obj):
            if obj["cmd"] == "getqrcode":
                resp = requests.post(
                    "https://tmonit.akasaki.space/api/vehicles/qrgenerate",
                    json=config_id,
                )
                return {"qrcode": resp.json()}
            return {}

        try:
            await send_nodes()
            # Client handler event loop:
            cache = {}
            while True:
                which_func, result = await tasks.next()
                if which_func == task_recv:
                    obj = json.loads(result)
                    if "requestId" in obj:
                        resp = await handle_request(obj)
                        resp["requestId"] = obj["requestId"]
                        await websocket.send(json.dumps(resp))
                    if obj["cmd"] == "requestImage":
                        image_requested = True
                    if obj["cmd"] == "videoEnabled":
                        image_enabled = obj["value"]
                elif which_func == task_sensors:
                    name, val = result
                    # print('sensors', name)
                    await websocket.send(json.dumps({name: val}))
                elif which_func == task_video:
                    if image_enabled != True and image_requested == False:
                        continue
                    image_requested = False
                    seq, image = result
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    shape = image.shape
                    if "task_imgseg" in cache:
                        # image = cache["task_imgseg"]*13
                        # todo wtf
                        image = cache["task_imgseg"]*image
                    buffer = image.tobytes("C")
                    await websocket.send(json.dumps({'image': {'w': shape[1], 'h': shape[0], 'seq': seq}}))
                    await websocket.send(buffer)
                elif which_func == task_points:
                    data = json.dumps(
                        {"lanePoints": [{"x": x, "y": y} for [x, y] in result]}
                    )
                    await websocket.send(data)
                elif which_func == task_targets:
                    await websocket.send(json.dumps({"targets": result}))
                elif which_func == task_imgseg:
                    cache["task_imgseg"] = result
                elif which_func == task_nodes:
                    await send_nodes()

        except ConnectionClosed:
            logger.log("Websocket client disconnected.")

    logger.log(f"Websocket serves at: {config['address']}" f":{config['port']}")
    await websockets.serve(
        client_handler, config["address"], config["port"], compression=None
    )
