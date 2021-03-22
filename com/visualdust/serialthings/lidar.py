from abc import ABC

from rplidar import RPLidar
from com.visualdust.serialthings.isensor import ISensor
from utils.logger import Logger

class Lidar(ISensor, ABC):
    def __init__(self, port, name="lidar"):
        self.lidar = RPLidar(port)
        self.lidar.reset()
        self._iter = self.lidar.iter_scans()
        super().__init__(name)
        self.logger = Logger(name)
        self.logger.log("Lidar initialized.")

    def _read(self):
        return self._iter.__next__()

