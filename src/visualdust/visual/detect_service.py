from src.visualdust.visual.ultra_fast_lane import LaneDetector
from utils.ufld_common import draw_result_on
from utils.logging import *
from utils.asynchelper import Event, Broadcaster
from threading import Thread
from src.visualdust.visual.cam_noneblocking import CameraThreadoo
import scipy.special
import numpy as np
import torch
import cv2
from src.visualdust.visual.ultra_fast_lane import LaneDetector


class LaneDetectService(Thread):
    detector: LaneDetector

    def __init__(this, lane_detector, capture_thread, capture_name, name="DetectService", print_on_screen=False):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.detector = lane_detector
        this.capture_thread = capture_thread
        this.capture_name = capture_name
        this.data_broadcaster = Broadcaster()
        this.print_on_screen = print_on_screen
        this.current = []
        this.logger.log("Ready.")

    def run(this) -> None:
        while True:
            frame = this.capture_thread.now(this.capture_name)
            """
            Test only
            """
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # frame = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
            # frame = np.stack((frame,) * 3, axis=-1)
            """
            Test only
            """
            out = this.detector.process(frame)
            out_converted = this.detector.convert_result(out, (frame.shape[0], frame.shape[1]))
            this.current = out_converted
            this.data_broadcaster.set_current(out_converted)
            # print("processed")
            if this.print_on_screen:
                cv2.imshow("LaneDetection on " + this.capture_name, draw_result_on(frame, out_converted))
                cv2.waitKey(10)

    def now(this):
        return this.current


class TargetDetectService(Thread):
    def __init__(this):
        Thread.__init__(this)
        # todo what to do
