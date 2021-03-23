from threading import Thread
from time import sleep
from typing import Dict
from utils.asynchelper import Event, run_in_event_loop, loop
from asyncio import create_task
from utils.logger import Logger
from .isensor import ISensor


class Hub(object):
    def __init__(this, name=None):
        if name is None:
            name = 'HUB-' + str(this)
        super(Hub, this).__init__()
        this.name = name
        this.logger = Logger(this)
        this.loop = False
        this.watching = {}
        this.event_update = Event(loop=loop)
        this.last_update = (None, None)
        this.values = {}
        this._clear_deferred = False

    def register(this, sensor):
        this.watching[sensor.name] = sensor
        this.logger.log("Attached new sensor: " + sensor.name)
        return this

    async def run_single(this, sensor: ISensor):
        while this.loop:
            val = await sensor.queue.get()
            this._set_update(sensor.name, val)
    
    async def get_update(this):
        await this.event_update.wait()
        return this.last_update

    def _set_update(this, name, val):
        this.values[name] = val
        this.last_update = (name, val)
        this.event_update.set_and_clear_threadsafe()

    def start(this) -> None:
        this.loop = True
        this.logger.log("Started to observe.")
        for key in this.watching:
            x = this.watching[key]
            create_task(this.run_single(this.watching[key]))

    def stop(this):
        this.loop = False

