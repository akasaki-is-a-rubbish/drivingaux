from src.visualdust.visual.detect_service import TargetDetectService
from src.visualdust.visual.you_only_look_once import TargetDetector
from src.visualdust.visual.detect_service import LaneDetectService
from src.visualdust.visual.cam_noneblocking import CameraThreadoo
from src.visualdust.visual.ultra_fast_lane import LaneDetector
from utils.logging import Logger, IconMode, IconColor
from src.visualdust.serialthings.hub import Hub
from utils.asynchelper import loop
from src.backend import socketo
import asyncio
import json
import cv2
import os, signal
import time

hub_config = json.load(open("./config/sensor.json"))
websockets_config = json.load(open("./config/websocket.json"))
vision_config = json.load(open("./config/vision.json"))

logger = Logger("Launcher", ic=IconMode.sakura, ic_color=IconColor.magenta)
logger.print_txt_file("data/com/visualdust/banner.txt").banner().print_os_info().banner()


async def check_sensor_values(hub):
    while len(hub.values.keys()) == 0:
        await hub.event_update.wait()
    logger.log(f"Sensor values ready")


# creating main task
async def main():

    # creating hub and register sensors
    hub = Hub.parse_config(hub_config)
    hub.start()

    # creating capture thread none blocking
    camera_service = CameraThreadoo()
    camera_service.register(cv2.VideoCapture(vision_config["video_capture"]), vision_config["observing_on"], True)
    camera_service.start()

    # creating lane detector
    lane_detector = LaneDetector(vision_config)
    lane_detect_service = LaneDetectService(lane_detector, camera_service, vision_config["observing_on"])
    lane_detect_service.start()

    # creating target detector
    target_detector = TargetDetector(vision_config)
    target_detector_service = TargetDetectService(target_detector, camera_service, vision_config["observing_on"],
                                                time_delay=0.1)
    target_detector_service.start()

    asyncio.create_task(socketo.websocket_serve(hub, lane_detect_service, camera_service, target_detector_service, websockets_config))
    asyncio.create_task(check_sensor_values(hub))
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
