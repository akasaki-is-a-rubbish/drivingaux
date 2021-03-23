import asyncio

def run_in_event_loop(func, *args):
    asyncio.get_event_loop().call_soon_threadsafe(func, *args)

class Event(asyncio.Event):

    def set_and_clear_threadsafe(this):
        asyncio.get_event_loop().call_soon_threadsafe(this.set_and_clear)

    def set_and_clear(this):
        this.set()
        this.clear()

    def set_threadsafe(this):
        asyncio.get_event_loop().call_soon_threadsafe(this.set)

    def clear_threadsafe(this):
        asyncio.get_event_loop().call_soon_threadsafe(this.clear)

class Queue(asyncio.Queue):

    def put_threadsafe(this, item):
        asyncio.get_event_loop().call_soon_threadsafe(this.put, item)
