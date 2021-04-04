import numpy as np
import scipy.special
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
from utils.yolo_common import *
from model.model import parsingNet
from utils.logging import *
from utils.general import *
from utils.datasets import *


class TargetDetector:
    def __init__(this, config):
        this.logger = Logger("YOLODetector-" + str(this.__hash__()), ic=IconMode.setting, ic_color=IconColor.cyan)
        this.logger.log("Loading weights...")
        ckpt_loaded = torch.load(config["model_yolo"])
        model = Ensemble()
        model.append(ckpt_loaded['ema' if ckpt_loaded.get('ema') else 'model'].float().fuse().eval())
        for m in model.modules():
            if type(m) in [torch.nn.Hardswish, torch.nn.LeakyReLU, torch.nn.ReLU, torch.nn.ReLU6, torch.nn.SiLU]:
                m.inplace = True  # pytorch 1.7.0 compatibility
            elif type(m) is Conv:
                m._non_persistent_buffers_set = set()  # pytorch 1.6.0 compatibility
        this.model = model[-1]
        if config["with_gpu"]:
            this.model.gpu()
        this.names = this.model.module.names if hasattr(this.model, 'module') else this.model.names
        this.logger.log("Ready.")

    def post_processing(this, pred, original_img_shape):
        result = []
        for i, det in enumerate(pred):  # detections per image
            if len(det):
                det[:, :4] = scale_coords(original_img_shape[1:], det[:, :4], original_img_shape).round()
                s = ""
                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {this.names[int(c)]}{'s' * (n > 1)}, "  # add to string
                print(s)
                result.append(det)
        return result

    def process(this, image):
        image = torch.from_numpy(image)
        if image.ndimension() == 3:
            image = image.unsqueeze(0)
        pred = this.model(image / 255.0)
        return this.post_processing(non_max_suppression(pred[0], agnostic=False), image.shape)
