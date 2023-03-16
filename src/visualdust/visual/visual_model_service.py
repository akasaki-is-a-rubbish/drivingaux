from .you_only_look_once import TargetDetector
from .ultra_fast_lane import LaneDetector
from .fast_seger import FastSegmentation

# from .monodepth_estimasion import DepthEstimator
from utils.logging import *
from utils.asynchelper import Event, Broadcaster
from threading import Thread
import time
import numpy as np
import cv2


class SegmentationService(Thread):
    processor: FastSegmentation

    def __init__(self, config, camera, time_delay=0.0, name="SegmentationProvider"):
        Thread.__init__(self)
        self.name = name
        self.logger = Logger(self.name, ic=IconMode.java, ic_color=IconColor.yellow)
        self.processor = FastSegmentation(config)
        self.capture = camera
        self.data_broadcaster = Broadcaster()
        self.current = []
        self.time_delay = time_delay
        self.logger.log("Ready.")

    def run(this) -> None:
        while True:
            _, frame = this.capture.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out = this.processor.process(frame)
            this.current = cv2.addWeighted(out, 0.5, frame, 0.5, 0.0)
            this.data_broadcaster.set_current(this.current)

    def now(this):
        return this.current


class LaneDetectService(Thread):
    processor: LaneDetector

    def __init__(
        this, config, camera_service, time_delay=0.0, name="LaneDetectService"
    ):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.processor = LaneDetector(config)
        this.capture_thread = camera_service
        this.capture_name = config["camera_name"]
        this.data_broadcaster = Broadcaster()
        this.current = []
        this.time_delay = time_delay
        this.logger.log("Ready.")

    def run(this) -> None:
        while True:
            frame = this.capture_thread.now(this.capture_name)
            out = this.processor.process(frame)
            out_converted = this.processor.convert_result(
                out, (frame.shape[0], frame.shape[1])
            )
            this.current = out_converted
            this.data_broadcaster.set_current(out_converted)
            time.sleep(this.time_delay)

    def now(this):
        return this.current


class TargetDetectService(Thread):
    processor: TargetDetector

    def __init__(
        this, config, camera_service, time_delay=0.0, name="TargetDetectService"
    ):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.processor = TargetDetector(config)
        this.capture_thread = camera_service
        this.capture_name = config["camera_name"]
        this.time_delay = time_delay
        this.data_broadcaster = Broadcaster()
        this.current = []
        this.logger.log("Ready.")

    def run(this) -> None:
        while True:
            frame = this.capture_thread.now(this.capture_name)
            out = this.processor.process(frame)
            this.current = out
            this.data_broadcaster.set_current(out)
            time.sleep(this.time_delay)

    def now(this):
        return this.current


# class MonoDepthEstimationService(Thread):
#     processor: DepthEstimator

#     def __init__(this, config, camera_service, time_delay=0., name="MonoDepthEstimationService"):
#         this.name = name
#         this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
#         this.processor = DepthEstimator(config)
#         this.capture_thread = camera_service
#         this.capture_name = config["camera_name"]
#         this.time_delay = time_delay
#         this.data_broadcaster = Broadcaster()
#         this.current = []
#         this.logger.log("Ready.")

#     def run(this) -> None:
#         while True:
#             frame = this.capture_thread.now(this.capture_name)
#             out = this.processor.process(frame)
#             this.current = out
#             this.data_broadcaster.set_current(out)
#             time.sleep(this.time_delay)

#     def now(this):
#         return this.current
