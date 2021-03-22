from threading import Thread
from time import sleep
from typing import Dict
import asyncio
from utils.logger import Logger


class Hub(object):
    def __init__(self, name=None):
        if name is None:
            name = 'HUB-' + str(self)
        super(Hub, self).__init__()
        self.name = name
        self.logger = Logger(name)
        self.loop = False
        self.watching = {}
        self.event_anyupdate = asyncio.Event()

    def register(self, sensor):
        self.watching[sensor.name] = sensor
        self.logger.log("Attached new sensor: " + sensor.name)
        return self

    async def run_single(self, sensor):
        while self.loop:
            SensorValue[sensor.name] = sensor.now()
            self.event_anyupdate.set()
            self.event_anyupdate.clear()
            # await sensor.event_read.wait()
            await asyncio.sleep(0.1)

    def start(self) -> None:
        self.loop = True
        self.logger.log("Started to observe.")
        for key in self.watching:
            asyncio.create_task(self.run_single(self.watching[key]))

    def stop(self):
        self.loop = False


SensorValue = {
}
