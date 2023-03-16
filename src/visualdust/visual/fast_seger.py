import torch
import torch.utils
import torch.nn.functional as F
import torchvision.transforms as ts
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from utils.logging import *
from models.lpsnet import get_lspnet_s
import collections


class FastSegmentation:
    def __init__(self, config):
        self.logger = Logger(
            "FastSegmentation-" + str(self.__hash__()),
            ic=IconMode.left_right,
            ic_color=IconColor.magenta,
        )
        self.logger.log("Parsing net...")
        self.net = get_lspnet_s(deploy=True)
        self.net.load_state_dict(torch.load(config["weight"], map_location="cpu"))
        self.net.eval()
        if "with_gpu" in config and config["with_gpu"]:
            self.with_gpu = True
            self.net = self.net.cuda()
        else:
            self.with_gpu = False
        self.transform_img = ts.Compose(
            [
                ts.ToTensor(),
                ts.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ]
        )

        def default_mapping_val():
            return 0

        self.label_mapping = collections.defaultdict(default_mapping_val)
        self.label_mapping.update(
            {
                10:0
            }
        )
        self.logger.log("Model ready.")

    def process(self, image):
        image = self.transform_img(image)
        image = image[None, :, :, :]
        if self.with_gpu:
            image = image.cuda()
        logit = self.net(image)
        pred = torch.argmax(
            F.interpolate(logit, size=(720, 1280), mode="bilinear", align_corners=True),
            dim=-3,
        )
        pred = pred.squeeze()
        pred = torch.swapaxes(torch.swapaxes(pred.repeat(3, 1, 1), 0, 1), 2, 1)
        return np.uint8(pred.cpu())

    def post_processing(this, pred):
        for key in this.label_mapping.keys():
            pred[pred == key] = this.label_mapping[key]
        return pred
