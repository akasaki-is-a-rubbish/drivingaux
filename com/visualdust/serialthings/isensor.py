from abc import abstractmethod
from threading import Thread
from asyncio import Event
from serial import Serial


class ISensor(Thread):
    def __init__(self, name=None, autostart=True):
        Thread.__init__(self, name=name)
        self.name = name
        self.current = {}
        self.loop = False
        self.event_read = Event()
        if autostart:
            self.start()

    def run(self) -> None:
        if self.loop:
            print("Already running:", self)
        self.loop = True
        while self.loop:
            self.current = self._read()
            self.event_read.set()
            self.event_read.clear()

    @abstractmethod
    def _read(self):
        # read and process data here
        pass

    def stop(self):
        self.loop = False

    def now(self) -> dict:
        return self.current
