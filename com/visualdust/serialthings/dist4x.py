from abc import ABC
from random import random

from isensor import *
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
        while this.serial.read().hex() != 'ff':
            pass
        varry = []
        for counter in range(8):
            varry.append(this.serial.read().hex())
        # print(varry)
        sensor_value = []
        sensor_value.append(int(varry[0], 16) * 256 + int(varry[1], 16))
        sensor_value.append(int(varry[2], 16) * 256 + int(varry[3], 16))
        sensor_value.append(int(varry[4], 16) * 256 + int(varry[5], 16))
        sensor_value.append(int(varry[6], 16) * 256 + int(varry[7], 16))
        sum = 0xff
        for element in varry:
            sum += int(element, 16)
        if sum & 0xff == int(this.serial.read().hex(), 16):
            # print("Sensor value : ", sensor_value)
            return {
                "s1": sensor_value[0],
                "s2": sensor_value[1],
                "s3": sensor_value[2],
                "s4": sensor_value[3]
            }
