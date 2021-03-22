from abc import ABC

from rplidar import RPLidar
from com.visualdust.serialthings.isensor import ISensor

class Lidar(ISensor, ABC):
    def __init__(self, port, name="lidar"):
        self.lidar = RPLidar(port)
        self.lidar.reset()
        self._iter = self.lidar.iter_scans()
        super().__init__(name)

    def _read(self):
        return self._iter.__next__()

