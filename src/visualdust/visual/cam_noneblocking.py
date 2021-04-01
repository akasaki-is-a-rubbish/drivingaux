from threading import Thread
from utils.logging import *
from time import sleep
from utils.asynchelper import *
from typing import Dict
import cv2


class CameraThreadoo(Thread):
    frames_broadcaster: Dict[str, Broadcaster]
    cams: Dict[str, cv2.VideoCapture]

    def __init__(this, name="CamNoneBlocking"):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(name,ic=IconMode.star_filled,ic_color=IconColor.red)
        this.cams = {}
        this.frames_broadcaster = {}
        this.delay = 0.03
        this.logger.log("Ready.")

    def register(this, video_capture, name):
        assert name is not None
        this.frames_broadcaster[name] = Broadcaster()
        this.cams[name] = video_capture
        this.logger.log(f"New video capture registered: {name}")

    def run(this) -> None:
        while True:
            for key, value in this.cams.items():
                ok, img = value.read()
                if ok:
                    this.frames_broadcaster[key].set_current(img)
            sleep(this.delay)

    def set_delay(this, delay):
        this.delay = delay

    def now(this, registered_name):
        assert registered_name is not None
        return this.frames_broadcaster[registered_name].current

    async def get_next(this, registered_name):
        assert registered_name is not None
        return await this.frames_broadcaster[registered_name].get_next()
