from threading import Thread
from time import sleep
from typing import Dict

import cv2

from utils.asynchelper import *
from utils.logging import *


class CameraService(Thread):
    frames_broadcaster: Dict[str, Broadcaster]
    cams: Dict[str, cv2.VideoCapture]

    def __init__(this, config: dict, name="CamNoneBlocking"):
        Thread.__init__(this)
        this.name = name
        this.logger = Logger(name, ic=IconMode.circle_filled, ic_color=IconColor.red)
        this.logger.log("Getting cameras ready...")
        this.cams = {}
        this.frames_broadcaster = {}
        this.print_on_screen = {}
        this.delay = 0.01
        for cam_name, cam_src in config.items():
            if not config[cam_name]["enabled"]:
                this.logger.log(
                    "Camera: " + cam_name + " at " + str(config[cam_name]["source"]) + " was set to beignored.")
                continue
            cap = cv2.VideoCapture(config[cam_name]["source"])
            if type(cam_src) != str:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            this.register(cap, cam_name, True)
            this.logger.log("Camera registered: " + cam_name + " at " + str(config[cam_name]["source"]))
        this.logger.log("Ready.")

    def register(this, video_capture: cv2.VideoCapture, name, wait_for_frame_ready=False, print_on_screen=False):
        assert name is not None
        this.frames_broadcaster[name] = Broadcaster()
        this.cams[name] = video_capture
        this.print_on_screen[name] = print_on_screen
        if wait_for_frame_ready:
            while video_capture.read() is None:
                sleep(0.1)
            this.logger.log(f"Capture({name}) ready.")

    def run(this) -> None:
        while True:
            for key, value in this.cams.items():
                ok, img = value.read()
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                if this.print_on_screen[key]:
                    cv2.imshow(key, img)
                    cv2.waitKey(10)
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
