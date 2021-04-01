from src.visualdust.visual.ultra_fast_lane import LaneDetector
from src.visualdust.visual.detect_service import LaneDetectService
from src.visualdust.visual.cam_noneblocking import CameraThreadoo
from utils.logging import Logger, IconMode, IconColor
from time import sleep
import json
import cv2

vision_config = json.load(open("./config/vision.json"))

logger = Logger("Launcher", ic=IconMode.sakura, ic_color=IconColor.magenta)
logger.print_txt_file("data/com/visualdust/banner.txt").banner().print_os_info().banner()

# creating capture thread none blocking
camera_service = CameraThreadoo()
camera_service.register(cv2.VideoCapture("/home/visualdust/Videos/4K Scenic Byway 12 _ All American Road in Utah, USA - 5 Hour of Road Drive with Relaxing Music-ZOZOqbK86t0.webm"),
                        "fronting")
camera_service.start()

# creating lane detector
detector = LaneDetector(vision_config)
lane_detect_service = LaneDetectService(detector, camera_service, "fronting", with_display=True)
lane_detect_service.start()

sleep(999999)
