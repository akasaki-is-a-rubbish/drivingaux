from threading import Thread
from utils.logging import *
from time import sleep
from utils.asynchelper import *
from typing import Dict
import cv2


class CameraThreadoo(Thread):
    def __init__(this, name="CamNoneBlocking"):
        super().__init__(name)
        this.name = name
        this.logger = Logger(name)
        this.cams: Dict[str, cv2.VideoCapture] = {}
        this.frames_broadcaster = {}
        this.delay = 0.03

    def register(this, video_capture, name=None):
        assert name is not None
        this.frames_broadcaster[name] = Broadcaster()
        this.cams[name] = video_capture

    def run(this) -> None:
        while True:
            for key, value in this.cams:
                this.frames_broadcaster[key].set_current(value.read())
            sleep(this.delay)

    def set_delay(this, delay):
        this.delay = delay

    def now(this, registered_name):
        assert registered_name is not None
        return this.frames_broadcaster[registered_name].current
