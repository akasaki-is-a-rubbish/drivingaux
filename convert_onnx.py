import json

import torch

from src.visualdust.visual.ultra_fast_lane import LaneDetector
from utils.logging import Logger, IconMode, IconColor

vision_config = json.load(open("./config/vision.json"))

logger = Logger("Launcher", ic=IconMode.sakura, ic_color=IconColor.magenta)
logger.print_txt_file("data/com/visualdust/banner.txt").banner().print_os_info().banner()

# creating lane detector
detector = LaneDetector(vision_config)
model = detector.net
print(model)
torch.onnx.export(model,
                  torch.rand(1, 3, 288, 800),
                  f="./model/culane_18_full.onnx",
                  verbose=True,
                  export_params=True,
                  opset_version=11)
logger.log("ONNX export finished.")
