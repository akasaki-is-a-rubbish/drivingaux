from threading import Thread
from utils.logging import *
from time import sleep


class CameraThreadoo(Thread):
    def __init__(this, name="CamNoneBlocking"):
        super().__init__(name)
        this.name = name
        this.logger = Logger(name)
        this.cams = {}
        this.frames = {}
        this.delay = 0.03

    def register(this, video_capture, name=None):
        assert name is not None
        this.cams[name] = video_capture

    def run(this) -> None:
        while True:
            for key, value in this.cams:
                this.frames[key] = value.read()
            sleep(this.delay)

    def set_delay(this, delay):
        this.delay = delay

    def now(this, registered_name=None):
        assert registered_name is not None
        return this.frames[registered_name]
