from src.visualdust.visual.you_only_look_once import TargetDetector
from utils.logging import *
from utils.asynchelper import Event, Broadcaster
from threading import Thread
import time
from src.visualdust.visual.ultra_fast_lane import LaneDetector


class LaneDetectService(Thread):
    detector_ufld: LaneDetector

    def __init__(this, config, camera_service, time_delay=0., name="LaneDetectService"):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.detector_ufld = LaneDetector(config)
        this.capture_thread = camera_service
        this.capture_name = config["camera_name"]
        this.data_broadcaster = Broadcaster()
        this.current = []
        this.time_delay = time_delay
        this.logger.log("Ready.")

    def run(this) -> None:
        while True:
            frame = this.capture_thread.now(this.capture_name)
            out = this.detector_ufld.process(frame)
            out_converted = this.detector_ufld.convert_result(out, (frame.shape[0], frame.shape[1]))
            this.current = out_converted
            this.data_broadcaster.set_current(out_converted)
            time.sleep(this.time_delay)

    def now(this):
        return this.current


class TargetDetectService(Thread):
    def __init__(this, config, capture_thread, time_delay=0., name="TargetDetectService"):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(this.name, ic=IconMode.java, ic_color=IconColor.yellow)
        this.detector_yolo = TargetDetector(config)
        this.capture_thread = capture_thread
        this.capture_name = config["camera_name"]
        this.time_delay = time_delay
        this.data_broadcaster = Broadcaster()
        this.current = []
        this.logger.log("Ready.")

    def run(this) -> None:
        while True:
            frame = this.capture_thread.now(this.capture_name)
            out = this.detector_yolo.process(frame)
            this.current = out
            this.data_broadcaster.set_current(out)
            time.sleep(this.time_delay)

    def now(this):
        return this.current
