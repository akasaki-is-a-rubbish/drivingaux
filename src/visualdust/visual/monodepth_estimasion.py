from utils.logging import *

class DepthEstimator:
    def __init__(this,config):
        this.logger = Logger("UFLDetector-" + str(this.__hash__()), ic=IconMode.setting, ic_color=IconColor.cyan)
        this.logger.log("Parsing net...")