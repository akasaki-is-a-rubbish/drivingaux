from src.visualdust.visual.ultra_fast_lane import LaneDetector
from utils.logger import *
from threading import Thread
import scipy.special
import numpy as np


class DetectService(Thread):
    def __init__(this, lane_detector, video_capture, name="DetectService"):
        cls_num_per_lane = 18
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.detector = lane_detector
        this.video_capture = video_capture


def start(this) -> None:
    while True:
        ret, frame = this.video_capture.read()
        img_w = frame.shape[1]
        img_h = frame.shape[0]

        out = this.detector.process(frame)


