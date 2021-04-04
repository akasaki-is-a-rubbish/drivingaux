import numpy as np
import scipy.special
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
from utils.yolo_common import *
from model.model import parsingNet
from utils.logging import *


class TargetDetector:
    def __init__(this, config):
        this.logger = Logger("YOLODetector-" + str(this.__hash__()), ic=IconMode.setting, ic_color=IconColor.cyan)
        this.logger.log("Loading weights...")
        model_loaded = torch.load(config["model_yolo"])
        this.model = model_loaded["model"].float()
        if config["with_gpu"]:
            this.model.gpu()
        this.model.eval()
        this.logger.log("Ready.")

    def process(this, image):
        pred = this.model(image)
        return non_max_suppression(pred)
