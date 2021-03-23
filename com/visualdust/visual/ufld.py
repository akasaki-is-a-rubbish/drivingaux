import torch, os, cv2
from com.cfzd.model.model import parsingNet
from com.cfzd.utils.common import merge_config
from com.cfzd.utils.dist_utils import dist_print
import torch
import scipy.special, tqdm
import numpy as np
import torchvision.transforms as transforms
from com.cfzd.data.dataset import LaneTestDataset
from com.cfzd.data.constant import culane_row_anchor, tusimple_row_anchor
from utils.logger import Logger


class LaneDetector:
    def __init__(self, config):
        self.logger = Logger(self)
        assert config["backbone"] in \
               ['18', '34', '50', '101', '152', '50next', '101next', '50wide', '101wide']
        self.net = parsingNet(pretrained=False,
                              backbone=config["backbone"],
                              cls_dim=(config["griding_num"] + 1,
                                       config["cls_num_per_lane"], 4),
                              use_aux=False)
        self.logger.log("Loading model...")
        self.state_dict = torch.load(config["model"], map_location='cpu')['model']
        self.compatible_state_dict = {}
        for k, v in self.state_dict.items():
            if 'module.' in k:
                self.compatible_state_dict[k[7:]] = v
            else:
                self.compatible_state_dict[k] = v
        self.net.load_state_dict(self.compatible_state_dict, strict=False)
        self.net.eval()
        self.logger.log("Model ready.")
        self.preprocessing_transform = transforms.Compose([
            transforms.Resize((288, 800)),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ])
        self.logger.log("Detector ready.")

    def now(self):
        pass

    def attach(self,video_source):
        pass