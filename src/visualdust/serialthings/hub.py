from threading import Thread
from time import sleep
from typing import Dict
from utils.asynchelper import Event, run_in_event_loop, loop
from asyncio import create_task
from utils.logging import *
from .isensor import ISensor
from src.visualdust.serialthings.util import *


class Hub(object):
    def __init__(this, name=None):
        if name is None:
            name = 'HUB-' + str(this)
        super(Hub, this).__init__()
        this.name = name
        this.logger = Logger("Hub-" + str(this.__hash__()), ic=IconMode.block, ic_color=IconColor.green)
        this.loop = False
        this.watching = {}
        this.event_update = Event()
        this.last_update = (None, None)
        this.values = {}

    def register(this, sensor):
        this.watching[sensor.name] = sensor
        this.logger.log("Attached new sensor: " + sensor.name)
        return this

    async def _run_single(this, sensor: ISensor):
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
        if this.loop:
            return
        this.loop = True
        this.logger.log("Started to observe.")
        for key in this.watching:
            x = this.watching[key]
            create_task(this._run_single(this.watching[key]))

    def stop(this):
        this.loop = False

    def parse_config(config):
        hub = Hub("HUB")
        for sensor in parse_all(config):
            hub.register(sensor)
        return hub
