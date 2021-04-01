from src.visualdust.visual.ultra_fast_lane import LaneDetector
from utils.ufld_common import draw_result_on
from utils.logging import *
from utils.asynchelper import Event, Broadcaster
from threading import Thread
import scipy.special
import numpy as np
import cv2

class LaneDetectService(Thread):
    def __init__(this, lane_detector, capture_thread, capture_name, name="DetectService", with_display=False):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.detector = lane_detector
        this.capture_thread = capture_thread
        this.capture_name = capture_name
        this.data_broadcaster = Broadcaster()
        this.with_display = with_display
        this.current = []
        this.logger.log("Ready.")

    def run(this) -> None:
        while True:
            frame = this.capture_thread.now(this.capture_name)
            out = this.detector.process(frame)
            out_converted = this.detector.convert_result(out, (frame.shape[0], frame.shape[1]))
            this.current = out_converted
            this.data_broadcaster.set_current(out_converted)
            # print("processed")
            if this.with_display:
                cv2.imshow(this.capture_name, draw_result_on(frame, out_converted))
                cv2.waitKey(10)

    def now(this):
        return this.current



class TargetDetectService(Thread):
    def __init__(this):
        Thread.__init__(this)
        # todo what to do
