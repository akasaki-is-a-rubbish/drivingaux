# -*- coding: UTF-8 -*-

import threading
import time
from .dahua_util import init_camera, get_frame, close_camera


class DahuaThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.frame_read = None
        self.loop = False
        self.get_image_ready = False
        self.fps = 0
        self.frame_count = 0
        self.last_time = time.time()
        self.stream_source, self.camera = init_camera()
        if self.stream_source is None or self.camera is None:
            print("相机连接失败！")
            exit(-1)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        self.loop=True
        while self.loop:
            self.frame_read = get_frame(self.stream_source)
            self.get_image_ready = True
            self.cal_fps()
        close_camera(self.stream_source, self.camera)

    def cal_fps(self):
        """
        计算帧率
        """
        self.frame_count = self.frame_count + 1
        if self.frame_count >= 100:
            cur_time = time.time()
            self.fps = self.frame_count / (cur_time - self.last_time)
            self.last_time = cur_time
            self.frame_count = 0

    def now(self):
        return self.frame_read

    def stop(self):
        """
        结束线程
        """
        self.loop = False
