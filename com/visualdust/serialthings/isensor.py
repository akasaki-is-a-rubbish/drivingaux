from abc import abstractmethod
from threading import Thread
from utils.asynchelper import Queue, run_in_event_loop
from serial import Serial


class ISensor:
    def __init__(this, name: str, autostart=True):
        this.thread = Thread(None, this.run, 'sensor-' + name)
        this.name = name
        this.current = {}
        this.loop = False
        this.queue = Queue(1)
        if autostart:
            this.thread.start()

    def run(this) -> None:
        if this.loop:
            print("Already running:", this)
        this.loop = True
        while this.loop:
            this.current = this._read()
            run_in_event_loop(this.queue.put, this.current)


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
