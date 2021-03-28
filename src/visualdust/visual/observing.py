from utils.logging import Logger
from threading import Thread
from src.visualdust.visual.detect_service import *


class Observer(Thread):
    def __init__(this, lane_detect_service: LaneDetectService, target_detect_service: TargetDetectService,
                 name="Observer"):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(name)
        # todo what to do
