from src.visualdust.visual.ultra_fast_lane import LaneDetector
from utils.ufld_common import draw_result_on
from utils.logging import *
from utils.asynchelper import Event, Broadcaster
from threading import Thread
import time
from src.visualdust.visual.cam_noneblocking import CameraThreadoo
import scipy.special
import numpy as np
import torch
import cv2
from src.visualdust.visual.ultra_fast_lane import LaneDetector


class LaneDetectService(Thread):
    detector_ufld: LaneDetector

    def __init__(this, lane_detector, capture_thread, capture_name, time_delay=0., name="LaneDetectService",
                 print_on_screen=False):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.detector_ufld = lane_detector
        this.capture_thread = capture_thread
        this.capture_name = capture_name
        this.data_broadcaster = Broadcaster()
        this.print_on_screen = print_on_screen
        this.current = []
        this.time_delay = time_delay
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
            out = this.detector_ufld.process(frame)
            out_converted = this.detector_ufld.convert_result(out, (frame.shape[0], frame.shape[1]))
            this.current = out_converted
            this.data_broadcaster.set_current(out_converted)
            time.sleep(this.time_delay)
            # print("processed")
            if this.print_on_screen:
                cv2.imshow("LaneDetection on " + this.capture_name, draw_result_on(frame, out_converted))
                cv2.waitKey(10)

    def now(this):
        return this.current


class TargetDetectService(Thread):
    def __init__(this, target_detector, capture_thread, capture_name, time_delay=0., name="TargetDetectService"):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.detector_yolo = target_detector
        this.capture_thread = capture_thread
        this.capture_name = capture_name
        this.time_delay = time_delay
        this.data_broadcaster = Broadcaster()
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
            out = this.detector_yolo.process(frame)
            out_converted = this.detector_yolo.convert_result(out)
            this.current = out_converted
            # todo what to do
            this.data_broadcaster.set_current(out_converted)
            time.sleep(this.time_delay)
            # if this.print_on_screen:
            #     cv2.imshow("LaneDetection on " + this.capture_name, draw_result_on(frame, out_converted))
            #     cv2.waitKey(10)

    def now(this):
        return this.current
