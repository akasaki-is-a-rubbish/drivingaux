import cv2

from model.model import parsingNet
import torch
import numpy as np
import torchvision.transforms as transforms
import scipy.special
from utils.logging import *
from PIL import Image


class LaneDetector:
    def __init__(this, config):
        this.logger = Logger("Detector-" + str(this.__hash__()), ic=IconMode.setting, ic_color=IconColor.cyan)
        assert config["backbone"] in \
               ['18', '34', '50', '101', '152', '50next', '101next', '50wide', '101wide']
        this.logger.log("Parsing net...")
        this.net = parsingNet(pretrained=False,
                              backbone=config["backbone"],
                              cls_dim=(config["griding_num"] + 1,
                                       config["cls_num_per_lane"], 4),
                              use_aux=False)
        this.griding_num = config["griding_num"]
        this.logger.log("Loading model...")
        this.state_dict = torch.load(config["model"], map_location='cpu')['model']
        this.compatible_state_dict = {}
        for k, v in this.state_dict.items():
            if 'module.' in k:
                this.compatible_state_dict[k[7:]] = v
            else:
                this.compatible_state_dict[k] = v
        this.net.load_state_dict(this.compatible_state_dict, strict=False)
        this.net.eval()
        this.logger.log("Model ready.")
        this.preprocess = transforms.Compose([
            transforms.Resize((288, 800)),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ])
        this.logger.log("Detector ready.")
        this.row_anchor = [121, 131, 141, 150, 160, 170, 180, 189, 199, 209, 219, 228, 238, 248, 258, 267,
                           277, 287]
        this.cls_num_per_lane = config["cls_num_per_lane"]
        col_sample = np.linspace(0, 800 - 1, this.griding_num)
        this.col_sample_w = col_sample[1] - col_sample[0]

    def process(this, image):
        if type(image) == np.ndarray:
            image = Image.fromarray(image)
        else:
            raise Exception(
                f"Unresolved input type: {type(image)}. {type(torch.Tensor)} and {type(np.ndarray)} are allowed.")
        return this.net(torch.reshape(torch.unsqueeze(this.preprocess(image), -1), (1, 3, 288, 800)))

    def convert_result(this, out, size_origin, size_processed=(288, 800)):
        img_h = size_origin[0]
        img_w = size_origin[1]

        out_j = out[0].data.cpu().numpy()
        out_j = out_j[:, ::-1, :]
        prob = scipy.special.softmax(out_j[:-1, :, :], axis=0)
        idx = np.arange(this.griding_num) + 1
        idx = idx.reshape(-1, 1, 1)
        loc = np.sum(prob * idx, axis=0)
        out_j = np.argmax(out_j, axis=0)
        loc[out_j == this.griding_num] = 0
        out_j = loc

        target_pos = []
        for i in range(out_j.shape[1]):
            if np.sum(out_j[:, i] != 0) > 2:
                for k in range(out_j.shape[0]):
                    if out_j[k, i] > 0:
                        target_pos.append((int(out_j[k, i] * this.col_sample_w * img_w / size_processed[1]) - 1,
                                           int(img_h * (this.row_anchor[this.cls_num_per_lane - 1 - k] /
                                                        size_processed[0])) - 1))
        return target_pos
