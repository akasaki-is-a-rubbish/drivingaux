import os

import matplotlib.pyplot as plt

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
filepath = "/home/visualdust/workspace/temp/22号Gl261胶质瘤石蜡标本/"
outpath = "/home/visualdust/Desktop/sample_out/with_max_and_min/"

counter = 1
# plt.figure(figsize=(30, 30))
for filename in os.listdir(filepath):
    if counter >= 612: break
    row = str(int(counter / 36) + 1)
    if len(row) == 1: row = "0" + row
    column = (counter) % 36
    if column == 0: column = 1
    column = str(column)
    if len(column) == 1: column = "0" + column
    filename = "第" + row + "排" + column + ".dat"
    file = open(filepath + filename)
    index = []
    axis_1 = []
    axis_2 = []
    last = -1.
    for line in file.readlines():
        vars = line.split(",")
        if float(vars[1]) > 12:
            continue
        if last > float(vars[1]):
            continue
        last = float(vars[1])
        index.append(int(vars[0]))
        axis_1.append(float(vars[1]))
        axis_2.append(float(vars[2]))


