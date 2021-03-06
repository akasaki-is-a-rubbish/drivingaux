from com.visualdust.serialthings.dist4x import *
from com.visualdust.serialthings.hub import Hub,SensorValue as SValues
from time import sleep
d4x_1 = Dist4x("/dev/ttyUSB1", 9600, "dist4x_1")
Hub("dist4xs").register(d4x_1).start()

while len(SValues.keys()) == 0:
    pass
print(SValues)
