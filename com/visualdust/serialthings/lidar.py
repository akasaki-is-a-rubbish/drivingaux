from abc import ABC

from rplidar import RPLidar
from com.visualdust.serialthings.isensor import ISensor
from utils.logger import *


class Lidar(ISensor, ABC):
    def __init__(this, port, name="lidar"):
        this.lidar = RPLidar(port)
        this.lidar.reset()
        this._iter = this.lidar.iter_scans()
        super().__init__(name)
        this.logger = Logger(f"Lidar-{name}",ic=IconMode.circle,ic_color=IconColor.yellow)
        this.logger.log("Lidar initialized.")

    def _read(this):
        return this._iter.__next__()
