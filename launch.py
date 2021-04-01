from src.visualdust.visual.ultra_fast_lane import LaneDetector
from src.visualdust.visual.detect_service import LaneDetectService
from src.visualdust.visual.cam_noneblocking import CameraThreadoo
from utils.logging import Logger, IconMode, IconColor

from src.visualdust.serialthings.hub import Hub
from src.backend import frontend_server
from utils.asynchelper import loop
import asyncio
import json
import cv2

hub_config = json.load(open("./config/sensor.json"))
websockets_config = json.load(open("./config/websocket.json"))
vision_config = json.load(open("./config/vision.json"))

logger = Logger("Launcher", ic=IconMode.sakura, ic_color=IconColor.magenta)
logger.print_txt_file("data/com/visualdust/banner.txt").banner().print_os_info().banner()

# creating hub and register sensors
hub = Hub.parse_config(hub_config)
# creating capture thread none blocking
camera_service = CameraThreadoo()
camera_service.register(cv2.VideoCapture(vision_config["video_capture"]), "fronting")
camera_service.start()

# creating lane detector
detector = LaneDetector(vision_config)
lane_detect_service = LaneDetectService(detector, camera_service, "fronting")
lane_detect_service.start()

async def check_sensor_values():
    while len(hub.values.keys()) == 0:
        await hub.event_update.wait()
    logger.log(f"Sensor values ready")


# creating main task
async def main():
    pass
    hub.start()
    asyncio.create_task(frontend_server.websocket_serve(hub, lane_detect_service, camera_service, websockets_config))
    asyncio.create_task(check_sensor_values())


logger.log("Ready. starting to loop...")
# loop all
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
loop.run_forever()
