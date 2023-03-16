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
from utils.datasets import cvt_cityscapes_idx_img_to_rgb


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
        self.label_mapping.update({10: 0})
        self.logger.log("Model ready.")

    def process(self, image):
        _input = self.transform_img(image)
        _input = _input[None, :, :, :]
        if self.with_gpu:
            _input = _input.cuda()
        logit = self.net(_input)
        pred = torch.argmax(
            F.interpolate(logit, size=(720, 1280), mode="bilinear", align_corners=True),
            dim=-3,
        )
        pred = pred.squeeze()
        for ignored_label in [0, 1, 3, 4, 5, 9, 10]:
            pred[pred == ignored_label] = 0
        pred = pred.cpu().numpy()
        # pred = np.repeat(pred[:, :, np.newaxis], 3, axis=2)
        color_mask = cvt_cityscapes_idx_img_to_rgb(pred)
        return color_mask

    def post_processing(this, pred):
        for key in this.label_mapping.keys():
            pred[pred == key] = this.label_mapping[key]
        return pred
