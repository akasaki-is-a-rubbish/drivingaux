from threading import Thread
from time import sleep
from typing import Dict
import asyncio
from utils.logger import Logger


class Hub(object):
    def __init__(this, name=None):
        if name is None:
            name = 'HUB-' + str(this)
        super(Hub, this).__init__()
        this.name = name
        this.logger = Logger(this)
        this.loop = False
        this.watching = {}
        this.event_anyupdate = asyncio.Event()
        this.values = {}

    def register(this, sensor):
        this.watching[sensor.name] = sensor
        this.logger.log("Attached new sensor: " + sensor.name)
        return this

    async def run_single(this, sensor):
        while this.loop:
            this.values[sensor.name] = sensor.now()
            this.event_anyupdate.set()
            this.event_anyupdate.clear()
            # await sensor.event_read.wait()
            await asyncio.sleep(0.1)

    def start(this) -> None:
        this.loop = True
        this.logger.log("Started to observe.")
        for key in this.watching:
            asyncio.create_task(this.run_single(this.watching[key]))

    def stop(this):
        this.loop = False

