from utils.yolo_common import *
from utils.logging import *
from utils.general import *
import torch
from utils.datasets import *


class TargetDetector:
    def __init__(this, config):
        this.logger = Logger("YOLODetector-" + str(this.__hash__()), ic=IconMode.setting, ic_color=IconColor.cyan)
        this.logger.log("Loading weights...")
        ckpt_loaded = torch.load(config["model_yolo"])
        model = Ensemble()
        model.append(ckpt_loaded['ema' if ckpt_loaded.get('ema') else 'model'].float().fuse().eval())
        for m in model.modules():
            if type(m) in [torch.nn.Hardswish, torch.nn.LeakyReLU, torch.nn.ReLU, torch.nn.ReLU6, torch.nn.SiLU]:
                m.inplace = True  # pytorch 1.7.0 compatibility
            elif type(m) is Conv:
                m._non_persistent_buffers_set = set()  # pytorch 1.6.0 compatibility
        this.model = model[-1]
        # if config["with_gpu"]:
        #     this.model.gpu()
        this.names = this.model.module.names if hasattr(this.model, 'module') else this.model.names
        this.logger.log("Ready.")

    def post_processing(this, pred, original_img_shape):
        result = []
        for i, det in enumerate(pred):  # detections per image
            s = ""
            if len(det):
                ## FIXME:
                # print('before scale', det[:, :4])
                det[:, :4] = scale_coords((384,640), det[:, :4], original_img_shape).round()
                # print('after scale', det[:, :4])

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {this.names[int(c)]}{'s' * (n > 1)}, "  # add to string
                det = det.tolist()
                for tx in det:
                    tx.append(this.names[int(tx[5])])
                    result.append(tx)
            if len(s):
                print(s.removesuffix(", "))
        return result

    def pre_processing(this, image):
        converted = letterbox(image)[0]
        # Convert
        converted = converted[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        converted = np.ascontiguousarray(converted)
        return converted

    def process(this, image):
        converted = this.pre_processing(image)
        converted = torch.from_numpy(converted)
        if converted.ndimension() == 3:
            converted = converted.unsqueeze(0)
        pred = this.model(converted / 255.0)
        return this.post_processing(non_max_suppression(pred[0], conf_thres=0.01, agnostic=False), image.shape)

    def convert_result(this,result):
        # todo what to do
        return result