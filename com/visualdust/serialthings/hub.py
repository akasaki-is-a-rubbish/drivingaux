from threading import Thread
from time import sleep


class Hub(Thread):
    def __init__(self, name, pickuptime=0.3, autostart=False):
        if name is None:
            name = 'HUB-' + str(self)
        super(Hub, self).__init__()
        self.name = name
        self.loop = False
        self.watching = {}
        self.picuptime = pickuptime
        if autostart:
            self.start()

    def register(self, sensor):
        self.watching[sensor.name] = sensor
        return self

    def run(self) -> None:
        self.loop = True
        while self.loop:
            sleep(self.picuptime)
            for key in self.watching:
                SensorValue[key] = self.watching[key].now()

    def stop(self):
        self.loop = False


SensorValue = {
}
