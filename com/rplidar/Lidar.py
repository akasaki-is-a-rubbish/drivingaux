from rplidar import RPLidar


class Lidar:
    def __init__(self, port, baudrate=115200):
        self.baudrate = baudrate
        self.port = port
        self.lidar = RPLidar(port)
