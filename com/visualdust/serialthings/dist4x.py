from abc import ABC
from random import random
from struct import unpack

from com.visualdust.serialthings.isensor import *
from utils.logger import Logger

class Dist4x(ISensor, ABC):
    def __init__(this, port, baudrate, name=None):
        if name is None:
            name = "Sensor#" + str(random())
        this.logger = Logger(this)
        this.serial = Serial(port, baudrate=baudrate, timeout=10)
        super(Dist4x, this).__init__(name)
        this.logger.log("ready.")

    def _read(this) -> dict:
        while this.serial.read()[0] != 0xff:
            pass
        buf = this.serial.read(8)
        sensor_value = unpack('>4H', buf) # decode as four 16-bit unsigned integers
        checksum = 0xff + sum(buf)
        if (checksum & 0xff) == this.serial.read()[0]:
            return {
                "s1": sensor_value[0],
                "s2": sensor_value[1],
                "s3": sensor_value[2],
                "s4": sensor_value[3]
            }
