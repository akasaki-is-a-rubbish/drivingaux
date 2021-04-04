from src.visualdust.visual.you_only_look_once import TargetDetector
import json

vision_config = json.load(open("./config/vision.json"))
detector = TargetDetector(vision_config)
