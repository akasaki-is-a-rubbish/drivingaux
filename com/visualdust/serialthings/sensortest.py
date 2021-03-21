from com.visualdust.serialthings.dist4x import *
from com.visualdust.serialthings.hub import Hub, SensorValue as SValues

d4x_1 = Dist4x("/dev/ttyUSB0", 9600, "dist4x_1")
hub = Hub("dist4xs").register(d4x_1)

import websockets
import asyncio
import json

async def hello(websocket, path):
    while True:
        await websocket.send(json.dumps(SValues))
        await asyncio.sleep(0.1)

async def main():
    # await asyncio.sleep(0.01)
    hub.run()
    while len(SValues.keys()) == 0:
        await asyncio.sleep(0.1)
    print(SValues)
    await websockets.serve(hello, "0.0.0.0", 8765)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
