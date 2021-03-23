from abc import abstractmethod
from threading import Thread
from utils.asynchelper import Queue, run_in_event_loop, loop
from serial import Serial


class ISensor:
    def __init__(this, name: str, autostart=True):
        this.thread = Thread(None, this.run, 'sensor-' + name)
        this.name = name
        this.current = {}
        this.loop = False
        this.queue = Queue(1, loop=loop)
        if autostart:
            this.start()

    def run(this) -> None:
        if this.loop:
            print("Already running:", this)
        this.loop = True
        while this.loop:
            this.current = this._read()
            this.queue.put_threadsafe(this.current)


    @abstractmethod
    def _read(this):
        # read and process data here
        pass
    
    def start(this):
        this.thread.start()

    def stop(this):
        this.loop = False

    def now(this) -> dict:
        return this.current
