from src.visualdust.visual.ultra_fast_lane import LaneDetector
from utils.logger import *


class DetectService(object):
    def __init__(this, lane_detector, video_source, name="DetectService"):
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.detector = lane_detector
        this.video_source = video_source
