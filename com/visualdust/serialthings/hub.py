from threading import Thread
from time import sleep
from typing import Dict
import asyncio



class Hub(Thread):
    def __init__(self, name, pickuptime=0.3, autostart=False):
        if name is None:
            name = 'HUB-' + str(self)
        super(Hub, self).__init__()
        self.name = name
        self.loop = False
        self.watching = {}
        self.picuptime = pickuptime
        self.event_anyupdate = asyncio.Event()
        if autostart:
            self.start()

    def register(self, sensor):
        self.watching[sensor.name] = sensor
        return self

    async def run_single(self, sensor):
        while self.loop:
            SensorValue[sensor.name] = sensor.now()
            self.event_anyupdate.set()
            self.event_anyupdate.clear()
            # await sensor.event_read.wait()
            await asyncio.sleep(0.1)

    def run(self) -> None:
        self.loop = True
        for key in self.watching:
            asyncio.create_task(self.run_single(self.watching[key]))

    def stop(self):
        self.loop = False


SensorValue = {
}
