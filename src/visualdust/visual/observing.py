from utils.logging import Logger
from threading import Thread
from src.visualdust.visual.detect_service import *


class Observer(Thread):
    def __init__(this, lane_detect_service: LaneDetectService, target_detect_service: TargetDetectService,
                 name="Observer"):
        Thread.__init__(this)
        this.target_detect_service = target_detect_service
        this.lane_detect_service = lane_detect_service
        this.name = name
        this.logger = Logger(name)
        # todo what to do
 
    def run(self) -> None:
        pass