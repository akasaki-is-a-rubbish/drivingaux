from abc import ABC
from random import random
from struct import unpack

from src.visualdust.serialthings.isensor import *
from utils.logging import *


class Dist4x(ISensor, ABC):
    def __init__(this, port, baudrate, name=None):
        if name is None:
            name = "Dist4x-" + str(random())
        this.logger = Logger(f"Dist4x-{name}", ic=IconMode.left_right, ic_color=IconColor.red)
        this.serial = Serial(port, baudrate=baudrate, timeout=10)
        super(Dist4x, this).__init__(name)
        this.logger.log("ready.")

    def _read(this) -> dict:
        while this.serial.read()[0] != 0xff:
            pass
        buf = this.serial.read(8)
        sensor_value = unpack('>4H', buf)  # decode as four 16-bit unsigned integers
        checksum = 0xff + sum(buf)
        if (checksum & 0xff) == this.serial.read()[0]:
            return {
                "s1": sensor_value[0],
                "s2": sensor_value[1],
                "s3": sensor_value[2],
                "s4": sensor_value[3]
            }
