import json
from time import sleep

import cv2

from src.visualdust.visual.cam_noneblocking import CameraService
from src.visualdust.visual.visual_model_service import LaneDetectService
from src.visualdust.visual.ultra_fast_lane import LaneDetector
from utils.logging import Logger, IconMode, IconColor

vision_config = json.load(open("./config/vision.json"))

logger = Logger("Launcher", ic=IconMode.sakura, ic_color=IconColor.magenta)
logger.print_txt_file("data/com/visualdust/banner.txt").banner().print_os_info().banner()

# creating capture thread none blocking
camera_service = CameraService()
capture = cv2.VideoCapture(vision_config["video_capture"])
camera_service.register(capture, "fronting", wait_for_frame_ready=True, print_on_screen=False)
camera_service.start()

# creating lane detector
detector = LaneDetector(vision_config)
lane_detect_service = LaneDetectService(detector, camera_service, "fronting", print_on_screen=True)
lane_detect_service.start()

sleep(999999)
