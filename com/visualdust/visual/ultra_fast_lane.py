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
from PIL import Image


class LaneDetector:
    def __init__(this, config):
        this.logger = Logger(this)
        assert config["backbone"] in \
               ['18', '34', '50', '101', '152', '50next', '101next', '50wide', '101wide']
        this.net = parsingNet(pretrained=False,
                              backbone=config["backbone"],
                              cls_dim=(config["griding_num"] + 1,
                                       config["cls_num_per_lane"], 4),
                              use_aux=False)
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

    def process(this, single):
        if type(single) == torch.Tensor:
            pass
        elif type(single) == np.ndarray:
            single = Image.fromarray(single)
        else:
            raise Exception(
                f"Unresolved input type: {type(single)}. {type(torch.Tensor)} and {type(np.ndarray)} are allowed.")
        return this.net(torch.reshape(torch.unsqueeze(this.preprocess(single), -1), (1, 3, 288, 800)))