from utils.logging import *
import cv2
import matplotlib
import numpy as np
from openvino.runtime import Core


def normalize_minmax(data):
    """Normalizes the values in `data` between 0 and 1"""
    return (data - data.min()) / (data.max() - data.min())


def convert_result_to_image(result, colormap="viridis"):
    """
    Convert network result of floating point numbers to an RGB image with
    integer values from 0-255 by applying a colormap.

    `result` is expected to be a single network result in 1,H,W shape
    `colormap` is a matplotlib colormap.
    See https://matplotlib.org/stable/tutorials/colors/colormaps.html
    """
    cmap = matplotlib.cm.get_cmap(colormap)
    result = result.squeeze(0)
    result = normalize_minmax(result)
    result = cmap(result)[:, :, :3] * 255
    result = result.astype(np.uint8)
    return result


def to_rgb(image_data) -> np.ndarray:
    """
    Convert image_data from BGR to RGB
    """
    return cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)


class DepthEstimator:
    def __init__(this, config):
        this.logger = Logger("UFLDetector-" + str(this.__hash__()), ic=IconMode.setting, ic_color=IconColor.cyan)
        this.logger.log("Parsing net...")
        this.ie = Core()
        this.model = this.ie.read_model(model=config["weight"], weights=config["weight"].with_suffix(".bin"))
        this.compiled_model = this.ie.compile_model(model=this.model, device_name="CPU")
        this.input_key = this.compiled_model.input(0)
        this.output_key = this.compiled_model.output(0)
        this.network_input_shape = list(this.input_key.shape)
        this.accepted_height, accepted_width = this.network_input_shape[2:]

    def process(this, image):
        resized_image = cv2.resize(src=image, dsize=(this.accepted_height, this.accepted_width))
        # reshape image to network input shape NCHW
        input_image = np.expand_dims(np.transpose(resized_image, (2, 0, 1)), 0)
        result = this.compiled_model([input_image])[this.output_key]
        # convert network result of disparity map to an image that shows
        # distance as colors
        result_image = convert_result_to_image(result=result)
        result_image = cv2.resize(result_image, image.shape[:2][::-1])
