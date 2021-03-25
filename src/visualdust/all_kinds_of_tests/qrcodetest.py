import random
import string


def rand_str_with_len_of(len):
    return ''.join(random.sample(string.ascii_letters + string.digits + string.ascii_letters + string.digits, len))


import qrcode
import matplotlib.pyplot as plt

path = "/home/visualdust/workspace/KexieOrg/bookshelf_qrcodes/"
import cv2
import os
from PIL import Image
import numpy as np


def make_into(count=1, path="./"):
    for i in range(count):
        randstr = rand_str_with_len_of(32)
        filename = randstr + ".jpg"
        if os.path.exists(path=path + filename):
            count -= 1
            continue
        image = qrcode.make("kexie_bookshelf_" + randstr)
        image.save(path + filename)


make_into(2333, path)
