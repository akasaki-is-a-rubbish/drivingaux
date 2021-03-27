from src.visualdust.visual.ultra_fast_lane import LaneDetector
from utils.ufld_common import draw_result_on
from utils.logger import *
from utils.asynchelper import Event, Broadcaster
from threading import Thread
import scipy.special
import numpy as np


class DetectService(Thread):
    def __init__(this, lane_detector, video_capture, name="DetectService"):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.detector = lane_detector
        this.video_capture = video_capture
        this.data_broadcaster = Broadcaster()
        this.logger.log("Ready.")

    def run(this) -> None:
        while True:
            this.video_capture.read()
            this.video_capture.read()
            this.video_capture.read()
            ret, frame = this.video_capture.read()
            out = this.detector.process(frame)
            out_converted = this.detector.convert_result(out, (frame.shape[0],frame.shape[1]))
            result: np.ndarray = draw_result_on(frame,out_converted)
            h, w, _ = result.shape
            this.data_broadcaster.set_current(((w, h), result.tobytes('C')))
