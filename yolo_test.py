from src.visualdust.visual.you_only_look_once import TargetDetector
import json
import torch
import cv2

vision_config = json.load(open("./config/vision.json"))
detector = TargetDetector(vision_config)

capture = cv2.VideoCapture(0)

def starto():
    while True:
        rat, image = capture.read()
        detector.process(image)


starto()
