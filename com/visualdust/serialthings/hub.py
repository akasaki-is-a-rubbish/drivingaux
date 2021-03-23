from threading import Thread
from time import sleep
from typing import Dict
from utils.asynchelper import Event, run_in_event_loop
from utils.logger import Logger
from .isensor import ISensor


class Hub(object):
    def __init__(this, name=None):
        if name is None:
            name = 'HUB-' + str(this)
        super(Hub, this).__init__()
        this.name = name
        this.logger = Logger(name)
        this.loop = False
        this.watching = {}
        this.event_update = Event()
        this.last_updates = []
        this.values = {}
        this._clear_defered = False

    def register(this, sensor):
        this.watching[sensor.name] = sensor
        this.logger.log("Attached new sensor: " + sensor.name)
        return this

    async def run_single(this, sensor: ISensor):
        while this.loop:
            val = await sensor.queue.get()
            this._add_update(sensor.name, val)
    
    async def get_updates(this):
        await this.event_update.wait()
        return this.last_updates.copy()


    def _add_update(this, name, val):
        this.values[name] = val
        this.last_updates.append((name, val))
        if this._clear_defered == False:
            this._clear_defered = True
            def clear():
                this.last_updates = []
                this._clear_defered = False
            run_in_event_loop(clear)

    def start(this) -> None:
        this.loop = True
        this.logger.log("Started to observe.")
        for key in this.watching:
            x = this.watching[key]
            asyncio.create_task(this.run_single(this.watching[key]))

    def stop(this):
        this.loop = False

