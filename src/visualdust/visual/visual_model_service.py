from .you_only_look_once import TargetDetector
from .ultra_fast_lane import LaneDetector
from .monodepth_estimasion import DepthEstimator
from utils.logging import *
from utils.asynchelper import Event, Broadcaster
from threading import Thread
import time


class LaneDetectService(Thread):
    processor: LaneDetector

    def __init__(this, config, camera_service, time_delay=0., name="LaneDetectService"):
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
            out_converted = this.processor.convert_result(out, (frame.shape[0], frame.shape[1]))
            this.current = out_converted
            this.data_broadcaster.set_current(out_converted)
            time.sleep(this.time_delay)

    def now(this):
        return this.current


class TargetDetectService(Thread):
    processor: TargetDetector

    def __init__(this, config, camera_service, time_delay=0., name="TargetDetectService"):
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


class MonoDepthEstimationService(Thread):
    processor: DepthEstimator

    def __init__(this, config, camera_service, time_delay=0., name="MonoDepthEstimationService"):
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.processor = DepthEstimator(config)
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
