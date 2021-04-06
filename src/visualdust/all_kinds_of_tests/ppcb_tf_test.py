from tensorflow.keras import Sequential
from tensorflow.python.data import Dataset
from tensorflow.keras import optimizers, layers, models, datasets
from data import mdataset
from math import *
import sys
import tensorflow as tf
import ml_util.gpu
import numpy as np

if __name__ == '__main__':
    print("Invoking main")

    data = mdataset.DataSet()
    train_x, train_y, evaluation_x, evaluation_y = data.split_into_train_set(train_data_ratio=0.7)

    # qualified = data.qualified_as_zero_one_array()
    # mat = data.no_nan_matrix(first_axis_is_column=False)

    ml_util.gpu.tensorflow_disable_gpu()

    model = models.Sequential([
        # layers.Flatten(),
        layers.Input(shape=len(data.vkeys())),
        layers.Dense(432, activation=tf.nn.relu),
        layers.Dense(256, activation=tf.nn.relu),
        layers.Dense(128, activation=tf.nn.relu),
        layers.Dense(64, activation=tf.nn.relu),
        layers.Dense(18, activation=tf.nn.relu),
        tf.keras.layers.Dense(2, activation=tf.nn.softmax)
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(train_x, train_y, epochs=2000)
    model.evaluate(evaluation_x, evaluation_y)

    # model.fit(mat, qualified, epochs=100)
    # model.evaluate(mat, qualified)
    # model.summary()

    source_data = model.predict(np.array(data.no_nan_matrix(variable_at_first_dimension=False))).transpose()
    qualification = data.qualified_as_zero_one_array().astype(bool)
    disqualification = np.invert(qualification)
    yes_total = np.count_nonzero(qualification)
    no_total = len(qualification) - yes_total

    evaluation = np.where(source_data[1] > source_data[0], 1, 0)
    yes_predicted_correct = np.count_nonzero(evaluation[qualification] == qualification[qualification])
    no_predicted_correct = np.count_nonzero(evaluation[disqualification] == qualification[disqualification])

    print(f'Evaluation: \nYes: {yes_predicted_correct} / {yes_total} ({yes_predicted_correct / yes_total * 100:.1f}%)')
    print(f'No: {no_predicted_correct} / {no_total} ({no_predicted_correct / no_total * 100:.1f}%)')

    compare_matrix = np.array(
        [
            *model.predict(np.array(data.no_nan_matrix(variable_at_first_dimension=False))).transpose(),
            data.qualified_as_zero_one_array()
        ]
    )

    while False:
        try:
            x = list(map(float, input().split()))
            x = (x * int(ceil(432 / len(x))))[:432]
            print(model.predict(np.array(x).reshape(1, 432)))
        except Exception as e:
            raise