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
from utils.datasets import cvt_seg_idx_img_to_rgb
import time


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
        self.transform_img = ts.Compose(
            [
                ts.ToTensor(),
                ts.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ]
        )
        self.label_mapper = torch.tensor([1,6,12],dtype=torch.uint8)
        
        if "with_gpu" in config and config["with_gpu"]:
            self.with_gpu = True
            self.net = self.net.cuda()
            self.label_mapper = self.label_mapper.cuda()
        else:
            self.with_gpu = False
        self.logger.log("Model ready.")
        

    def process(self, image):
        _input = self.transform_img(image)
        if self.with_gpu:
            _input = _input.cuda()
        _input = _input[None, :, :, :]
        pred = self.net(_input)
        pred = torch.argmax(
            F.interpolate(pred, size=(720, 1280), mode="bilinear", align_corners=True),
            dim=-3,
        )
        pred = pred.type(torch.uint8)
        pred = pred.squeeze()
        for ignored_label in [0, 1, 3, 4, 5, 9, 10]:
            pred[pred == ignored_label] = 0
        pred = torch.stack((pred,) * 3, dim=-1) * self.label_mapper
        
        color_mask = pred.cpu().numpy()  # todo 0.01s
        # pred = np.repeat(pred[:, :, np.newaxis], 3, axis=2)
        # stacked_img = np.stack((color_mask,)*3, axis=-1)
        # color_mask = cvt_seg_idx_img_to_rgb(color_mask) # todo 0.032s
        return color_mask
