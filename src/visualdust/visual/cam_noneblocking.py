from threading import Thread
from time import sleep
from typing import Dict

import cv2

from utils.asynchelper import *
from utils.logging import *


class CameraThreadoo(Thread):
    frames_broadcaster: Dict[str, Broadcaster]
    cams: Dict[str, cv2.VideoCapture]

    def __init__(this, name="CamNoneBlocking"):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(name, ic=IconMode.star_filled, ic_color=IconColor.red)
        this.cams = {}
        this.frames_broadcaster = {}
        this.delay = 0.03
        this.logger.log("Ready.")

    def register(this, video_capture: cv2.VideoCapture, name, wait_for_frame_ready=False):
        assert name is not None
        this.frames_broadcaster[name] = Broadcaster()
        this.cams[name] = video_capture
        this.logger.log(f"New video capture registered: {name}")
        if wait_for_frame_ready:
            this.logger.log(f"Waiting for capture({name})...")
            while video_capture.read() is None:
                sleep(0.1)
            this.logger.log(f"Capture({name}) ready.")

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
