from abc import abstractmethod
from threading import Thread

from serial import Serial


class ISensor(Thread):
    def __init__(self, port, baudrate, name=None, autostart=True):
        Thread.__init__(self, name=name)
        self.serial = Serial(port, baudrate=baudrate, timeout=10)
        self.current = {}
        self.loop = False
        if autostart:
            self.start()

    def run(self) -> None:
        if self.loop:
            print("Already running:", self)
        self.loop = True
        while self.loop:
            self.current = self._read()

    @abstractmethod
    def _read(self) -> dict:
        # read and process data here
        pass

    def stop(self):
        self.loop = False

    def now(self) -> dict:
        return self.current
