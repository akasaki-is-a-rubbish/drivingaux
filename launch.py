import asyncio
import json

import websockets

from com.visualdust.serialthings.hub import Hub, SensorValue as SValues
from com.visualdust.serialthings.lidar import Lidar

# d4x_1 = Dist4x("/dev/ttyUSB0", 9600, "dist4x_1")
# hub = Hub("dist4xs").register(d4x_1)
lidar = Lidar("/dev/ttyUSB0")
hub = Hub("?").register(lidar)


async def client_handler(websocket, path):
    while True:
        await websocket.send(json.dumps(SValues))
        await asyncio.sleep(0.1)


async def socket_serve():
    # await asyncio.sleep(0.01)
    hub.run()
    while len(SValues.keys()) == 0:
        await asyncio.sleep(0.1)
    # print(SValues)
    await websockets.serve(client_handler, "0.0.0.0", 8765)


loop = asyncio.get_event_loop()
loop.run_until_complete(socket_serve())
loop.run_forever()
