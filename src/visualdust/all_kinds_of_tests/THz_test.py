import os

# import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
filepath = "/home/visualdust/workspace/temp/22号Gl261胶质瘤石蜡标本/"
outpath = "/home/visualdust/Desktop/sample_out/with_max_and_min/"

def __parseList__(str_lines):
    index = []
    axis_1 = []
    axis_2 = []
    last = -1.
    for line in str_lines:
        vars = line.split(",")
        last = float(vars[1])
        index.append(int(vars[0]))
        axis_1.append(float(vars[1]))
        axis_2.append(float(vars[2]))
    return [axis_1, axis_2]


def __read_all__(path):
    counter = 1
    pixeldata = np.zeros((17, 36, 2, 301), dtype=np.float)
    print(len(os.listdir(path)))
    for filename in os.listdir(path):
        if not filename.endswith(".dat"): continue
        row = filename[1] + filename[2]
        column = filename[4] + filename[5]
        pixel = np.array(__parseList__(open(filepath + filename).readlines()))
        pixeldata[int(row) - 1, int(column) - 1] = pixel
    return pixeldata


# def __read_db_from_folder__(path):
#     return tf.data.Dataset.from_tensor_slices(__read_all__(path))


pixel_data = __read_all__(filepath)
row_count = (pixel_data.shape)[0]
column_count = (pixel_data.shape)[1]
plt.figure(figsize=(25, 25))
for row in range(row_count):
    for column in range(column_count):
        axis_1, axis_2 = pixel_data[row, column]
        plt.subplot(row_count, column_count, row * 36 + column + 1)
        plt.ylabel = None
        plt.xlabel = None
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')
        plt.plot(axis_1, axis_2)
        # print(row,column)
        # max_x = max(axis_1)
        # min_x = min(axis_1)
        # max_y = max(axis_2)
        # min_y = min(axis_2)
        # plt.hlines(max_y, label="max", xmin=min_x, xmax=max_x, data=max_y, colors='r')
        # plt.text(min_x, max_y, 'max=' + str(max_y), ha='left', va='center')
        # plt.hlines(min_y, label="min", xmin=min_x, xmax=max_x, data=min_y, colors='g')
        # plt.text(min_x, min_y, 'max=' + str(min_y), ha='left', va='center')
plt.show()
