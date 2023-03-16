import threading
from src.visualdust.visual.visual_model_service import TargetDetectService
from src.visualdust.visual.visual_model_service import LaneDetectService
from src.visualdust.visual.visual_model_service import SegmentationService
from src.visualdust.visual.cam_noneblocking import CameraService
from utils.logging import Logger, IconMode, IconColor
from src.visualdust.serialthings.hub import Hub
from utils.asynchelper import loop
from src.backend import socketo, node
import asyncio
import json
import os, signal
import time

logger = Logger("Launcher", ic=IconMode.sakura, ic_color=IconColor.magenta)
logger.print_txt_file(
    "data/com/visualdust/banner.txt"
).banner().print_os_info().banner()


async def check_sensor_values(hub):
    while len(hub.values.keys()) == 0:
        await hub.event_update.wait()
    logger.log(f"Sensor values ready")


# creating main task
async def main():
    # starting the vehicle network node
    websockets_config = json.load(open("./config/websocket.json"))
    threading.Thread(None, node.init, args=[websockets_config["nodeName"]]).start()

    vision_config = json.load(open("./config/vision.json"))

    # creating capture thread none blocking
    camera_service = CameraService(vision_config["cameras"])

    image_segmentation_service = SegmentationService(vision_config["models"]["fast_segmentation"], camera_service.cams['camera_video'])
    image_segmentation_service.start()

    asyncio.create_task(
        socketo.websocket_serve(
            segmentation_provider=image_segmentation_service,
            config=websockets_config,
        )
    )
    logger.log("Services ready.")


try:
    # loop all
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.run_forever()
except Exception as e:
    print(e, flush=True)
finally:
    time.sleep(0.1)
    os.kill(os.getpid(), signal.SIGTERM)
