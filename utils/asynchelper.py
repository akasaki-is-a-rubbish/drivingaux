import asyncio
from typing import List, Callable, Coroutine

# Use a single loop from all threads
loop = asyncio.new_event_loop()


def run_in_event_loop(func, *args):
    loop.call_soon_threadsafe(func, *args)


class Event(asyncio.Event):
    "Thread-safe version of asyncio.Event"

    def __init__(this):
        asyncio.Event.__init__(this, loop=loop)

    def set_and_clear_threadsafe(this):
        loop.call_soon_threadsafe(this.set_and_clear)

    def set_and_clear(this):
        this.set()
        this.clear()

    def set_threadsafe(this):
        loop.call_soon_threadsafe(this.set)

    def clear_threadsafe(this):
        loop.call_soon_threadsafe(this.clear)


class Queue(asyncio.Queue):
    "Thread-safe version of asyncio.Queue"

    def __init__(this, maxsize=0):
        asyncio.Queue.__init__(this, maxsize, loop=loop)

    def put_threadsafe(this, item):
        loop.call_soon_threadsafe(lambda: asyncio.create_task(this.put(item)))


class Broadcaster(object):
    
    def __init__(this):
        this.event_update = Event()
        this.current = None

    def set_current(this, val):
        """Set current value (called from ANY thread)"""
        this.current = val
        this.event_update.set_and_clear_threadsafe()

    async def get_next(this):
        """Wait until the value updated and return it (called from asyncio code ONLY)"""
        await this.event_update.wait()
        return this.current


class TaskStreamMultiplexer(object):

    def __init__(this, funcs: List[Callable[[], Coroutine]]):
        this._funcs: List[(Callable[[], Coroutine], asyncio.Task)] = [(x, None) for x in funcs]

    async def next(this):
        for i, item in enumerate(this._funcs):
            func, task = item
            if task == None:
                task = asyncio.create_task(func())
                this._funcs[i] = (func, task)
            elif task.done():
                this._funcs[i] = (func, None)
                return (func, task.result())

        done, pending = await asyncio.wait([task for (func, task) in this._funcs], return_when=asyncio.FIRST_COMPLETED)

        for i, item in enumerate(this._funcs):
            func, task = item
            if task.done():
                this._funcs[i] = (func, None)
                return (func, task.result())
