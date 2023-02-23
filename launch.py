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
logger.print_txt_file("data/com/visualdust/banner.txt").banner().print_os_info().banner()


async def check_sensor_values(hub):
    while len(hub.values.keys()) == 0:
        await hub.event_update.wait()
    logger.log(f"Sensor values ready")


# creating main task
async def main():
    # starting the vehicle network node
    websockets_config = json.load(open("./config/websocket.json"))
    threading.Thread(None, node.init, args=[websockets_config['nodeName']]).start()

    # creating hub and register sensors
    hub_config = json.load(open("./config/sensor.json"))
    sensor_hub = Hub.parse_config(hub_config)
    sensor_hub.start()

    vision_config = json.load(open("./config/vision.json"))

    # creating capture thread none blocking
    camera_service = CameraService(vision_config["cameras"])
    camera_service.start()

    # creating lane detector
    lane_detect_service = LaneDetectService(vision_config["models"]["ultra_fast_lane"], camera_service, time_delay=0.05)
    lane_detect_service.start()

    # creating target detector
    target_detector_service = TargetDetectService(vision_config["models"]["yolo_target_detection"], camera_service)
    target_detector_service.start()

    image_segmentation_service = SegmentationService(vision_config["models"]["fast_segmentation"], camera_service)
    image_segmentation_service.start()

    asyncio.create_task(
        socketo.websocket_serve(sensor_hub, lane_detect_service, camera_service, image_segmentation_service,
                                websockets_config))
    asyncio.create_task(check_sensor_values(sensor_hub))
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
