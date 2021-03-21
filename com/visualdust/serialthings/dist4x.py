from abc import ABC
from random import random
from isensor import *


class Dist4x(ISensor, ABC):
    def __init__(self, port, baudrate, name=None):
        if name is None:
            name = "Sensor#" + str(random())

        super(Dist4x, self).__init__(port, baudrate, name)

    def _read(self) -> dict:
        while self.serial.read().hex() != 'ff':
            pass
        varry = []
        for counter in range(8):
            varry.append(self.serial.read().hex())
        # print(varry)
        sensor_value = []
        sensor_value.append(int(varry[0], 16) * 256 + int(varry[1], 16))
        sensor_value.append(int(varry[2], 16) * 256 + int(varry[3], 16))
        sensor_value.append(int(varry[4], 16) * 256 + int(varry[5], 16))
        sensor_value.append(int(varry[6], 16) * 256 + int(varry[7], 16))
        sum = 0xff
        for element in varry:
            sum += int(element, 16)
        if sum & 0xff == int(self.serial.read().hex(), 16):
            # print("Sensor value : ", sensor_value)
            return {
                "s1": sensor_value[0],
                "s2": sensor_value[1],
                "s3": sensor_value[2],
                "s4": sensor_value[3]
            }
