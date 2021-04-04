from src.visualdust.visual.you_only_look_once import TargetDetector
import json
import torch
import cv2

vision_config = json.load(open("./config/vision.json"))
detector = TargetDetector(vision_config)


def read_4d_frame(capture):
    rat, image = capture.read()
    # image = torch.unsqueeze(torch.Tensor(image), -1)
    # image = image.reshape((1, 3, 640, 480))
    return image


capture = cv2.VideoCapture(0)

def starto():
    while True:
        inp = read_4d_frame(capture)
        out = detector.process(inp)