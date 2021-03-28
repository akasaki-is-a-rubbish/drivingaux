from src.visualdust.visual.camlike import Camlike
from utils.logging import Logger

class Camera(Camlike):
    def __init__(this,device):
        this.device = device
        this.logger = Logger(this)
